import os
import asyncio
import logging
import argparse
from dotenv import load_dotenv
from opentelemetry import trace
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
# Import agent factories
from agents.sub_agent_factory import SubAgentFactory
from agents.orchestrator_agent import OrchestratorAgentFactory

# Load environment variables
load_dotenv()
# Set environment variable before instrumentation
os.environ["OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"] = "true"

# Initialize OpenAI instrumentation
OpenAIInstrumentor().instrument()

# Initialize tracer
tracer = trace.get_tracer(__name__)
# Use the connection string from environment variable as fallback
connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
configure_azure_monitor(connection_string=connection_string)

# No FastAPI app in the original version

@tracer.start_as_current_span("initialize_kernel")
def initialize_kernel():
    """
    Initialize the Semantic Kernel with Azure OpenAI configuration
    """
    span = trace.get_current_span()
    span.set_attribute("message", "Initializing Semantic Kernel")
    
    kernel = Kernel()
    
    # Configure AI service using environment variables
    deployment = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = "2024-10-21"
    
    # Add Azure OpenAI chat completion service
    kernel.add_service(
        AzureChatCompletion(
            service_id="chat_completion",
            deployment_name=deployment,
            endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
    )
    
    span.set_attribute("kernel_initialized", True)
    span.set_attribute("model_deployment", deployment)
    
    return kernel

@tracer.start_as_current_span("initialize_agents")
def initialize_agents(kernel) -> ChatCompletionAgent:
    """
    Initialize the orchestrator and specialized agents
    """
    span = trace.get_current_span()
    span.set_attribute("message", "Initializing agents")
    
    # Create specialized agents
    light_agent = SubAgentFactory.create_agent(kernel, "light")
    gardener_agent = SubAgentFactory.create_agent(kernel, "gardener")

    # Create orchestrator agent with specialized agents
    orchestrator_agent = OrchestratorAgentFactory.create_orchastrator_agent(
        kernel=kernel,
        sub_agents=[light_agent, gardener_agent]
    )
    
    span.set_attribute("agents_created", 3)
    
    return orchestrator_agent

# No API dependencies in the original version

@tracer.start_as_current_span("console_app")
async def console_app():
    # Set message attribute for the main span
    span = trace.get_current_span()
    span.set_attribute("message", "Multi-agent application running in console mode")
    
    print("Multi-agent system initialized. Starting chat session...")
    print("Type 'exit' to quit.")
    
    # Initialize kernel and agents
    kernel = initialize_kernel()
    orchestrator_agent = initialize_agents(kernel)
    
    # Get parent span for the entire conversation session
    parent_span = trace.get_current_span()
    parent_span.set_attribute("app_type", "multi_agent_system")
    parent_span.set_attribute("agent_count", 3)  # Orchestrator, Light and Plant agents
    
    conversation_id = f"conversation-{os.urandom(4).hex()}"
    parent_span.set_attribute("conversation_id", conversation_id)
    
    # Initialize thread to maintain conversation history
    thread = ChatHistoryAgentThread()
    
    turn_count = 0
    
    while True:
        user_input = input("You: ")
        turn_count += 1
        
        if user_input.lower() == 'exit':
            print("Exiting chat...")
            parent_span.set_attribute("total_turns", turn_count - 1)
            break
        
        with tracer.start_as_current_span(f"turn_{turn_count}"):
            turn_span = trace.get_current_span()
            turn_span.set_attribute("turn_number", turn_count)
            turn_span.set_attribute("conversation_id", conversation_id)
            turn_span.set_attribute("user_input", user_input)
            turn_span.set_attribute("message", f"Turn {turn_count}: {user_input}")
            
            # Process request through orchestrator agent
            with tracer.start_as_current_span("process_request"):
                process_span = trace.get_current_span()
                process_span.set_attribute("message", "Processing request through orchestrator")
                
                # Pass the user input to the orchestrator agent with the thread for history
                # Using await since this is an async method
                response = await orchestrator_agent.get_response(messages=user_input, thread=thread)
                
                # Extract the message content from the response
                assistant_message = str(response)
                
                # Record response metrics
                turn_span.set_attribute("response_length", len(assistant_message))
                turn_span.set_attribute("response_summary", assistant_message[:50] + "..." if len(assistant_message) > 50 else assistant_message)
            
            # Print response to user
            print(f"Assistant: {assistant_message}")

@tracer.start_as_current_span("main")
async def main():
    """Main entry point for the application"""
    # Run in console mode directly
    await console_app()

if __name__ == "__main__":
    # Use asyncio.run to run the async main function
    asyncio.run(main())
