from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from typing import List
from azure.ai.agents.telemetry import trace_function
from tools.light_tool import LightTool

class LightAgentFactory:
    
    @trace_function()
    def create_agent(kernel: Kernel) -> ChatCompletionAgent:
        # Clone the kernel
        agent_kernel = kernel.clone()
        
        # Add the light tool to the agent's kernel
        light_tool = LightTool()
        agent_kernel.add_plugin(light_tool, "LightTool")
        
        settings = AzureChatPromptExecutionSettings(
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
        )
        
        agent = ChatCompletionAgent(
            kernel=agent_kernel,
            name="LightAgent",
            instructions="""
                You are a specialized agent for managing smart lights in a home.
                You can check the status of lights, turn them on or off, adjust brightness, and change colors.
                
                When responding to light-related queries:
                1. First determine which light the user is referring to by name or ID
                2. Check the current state of the light using get_lights or get_state
                3. Perform the requested action if needed using change_state
                4. Always confirm what you've done or found in simple, clear language
                
                RESPONSE FORMAT:
                - Use plain, conversational language for your responses
                - Confirm the action taken and the current state
                - If changing a light's state, confirm the new settings (on/off, brightness, color)
                - Keep your responses concise and friendly
            """,
            arguments=KernelArguments(settings)
        )
        
        return agent
