from typing import List
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.functions import KernelArguments
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from azure.ai.agents.telemetry import trace_function

class OrchestratorAgentFactory:

    @trace_function()
    def create_orchastrator_agent(kernel: Kernel, sub_agents: List[ChatCompletionAgent]) -> ChatCompletionAgent:
        # Clone kernel
        agent_kernel = kernel.clone()

        # Add sub-agents to the kernel
        for agent in sub_agents:
            agent_kernel.add_plugin(agent, agent.name)

        settings = AzureChatPromptExecutionSettings(
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
        )

        agent = ChatCompletionAgent(
            kernel=agent_kernel,
            name="OrchestratorAgent",
            instructions="""
                You are a helpful assistant that coordinates between specialized agents to answer user questions 
                and perform tasks in a smart home environment. Your job is to determine which agent is best suited to handle each user request.
                
                AGENT SELECTION GUIDELINES:
                - For questions about lights, light status, controlling lights: Use LightAgent
                - For questions about plants, gardening, plant care, watering: Use GardenerAgent
                - If a query spans multiple domains, coordinate responses from multiple agents
                
                RESPONSE FORMAT:
                - Always respond in markdown format
                - Begin your response with a clear, direct answer to the user's query
                - If you used a specialized agent, attribute the information source: "According to [AgentName]..."
                - At the end of your response, include 3 useful follow-up questions or commands
                - For follow-ups, format as: "**Follow-up suggestions:**" followed by a numbered list
            """,
            arguments=KernelArguments(settings)
        )

        return agent
