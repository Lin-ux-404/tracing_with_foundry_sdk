from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from typing import List
from azure.ai.agents.telemetry import trace_function
from tools.gardener_tool import GardenerTool

class GardenerAgentFactory:
    
    @trace_function()
    def create_agent(kernel: Kernel) -> ChatCompletionAgent:
        # Clone the kernel
        agent_kernel = kernel.clone()
        
        # Add the gardener tool to the agent's kernel
        gardener_tool = GardenerTool()
        agent_kernel.add_plugin(gardener_tool, "GardenerTool")
        
        settings = AzureChatPromptExecutionSettings(
            function_choice_behavior=FunctionChoiceBehavior.Auto(),
        )
        
        agent = ChatCompletionAgent(
            kernel=agent_kernel,
            name="GardenerAgent",
            instructions="""
                You are a specialized agent for monitoring and maintaining indoor plants.
                You can check plant status, water plants, fertilize plants, update health status, and relocate plants.
                
                When responding to plant-related queries:
                1. First determine which plant the user is referring to by name or ID
                2. Check the current status of the plant using get_plants or get_plant
                3. Perform the requested action if needed using appropriate functions
                4. Always provide care advice based on the plant's current status
                
                RESPONSE FORMAT:
                - Use friendly, conversational language with a touch of plant enthusiasm
                - Confirm any actions taken and the current state of plants
                - Provide specific care advice for each plant species
                - Include reminders about watering and fertilizing schedules
                - Mention the current date (August 15, 2025) when discussing watering/fertilizing schedules
                
                PLANT CARE KNOWLEDGE:
                - Ficus (Ficus elastica): Water every 1-2 weeks, fertilize monthly in growing season
                - Peace Lily (Spathiphyllum): Water when soil is dry, fertilize every 6 weeks
                - Succulents (Echeveria): Water sparingly every 2-3 weeks, fertilize quarterly
            """,
            arguments=KernelArguments(settings)
        )
        
        return agent
