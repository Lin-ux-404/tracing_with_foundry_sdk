from typing import Dict, List, Literal, Optional
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatPromptExecutionSettings
from semantic_kernel.functions import KernelArguments
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from azure.ai.agents.telemetry import trace_function
from tools.light_tool import LightTool
from tools.gardener_tool import GardenerTool

# Define agent types
AgentType = Literal["light", "gardener"]

class SubAgentFactory:
    """
    Factory class for creating various specialized sub-agents.
    This replaces the individual factory classes for each agent type.
    """
    
    @staticmethod
    @trace_function()
    def create_agent(kernel: Kernel, agent_type: AgentType) -> ChatCompletionAgent:

        agent_kernel = kernel.clone()
        
        # Configure agent based on type
        if agent_type == "light":
            return SubAgentFactory._create_light_agent(agent_kernel)
        elif agent_type == "gardener":
            return SubAgentFactory._create_gardener_agent(agent_kernel)
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
    
    @staticmethod
    @trace_function()
    def _create_light_agent(agent_kernel: Kernel) -> ChatCompletionAgent:
        """Create a light management agent"""
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
    
    @staticmethod
    @trace_function()
    def _create_gardener_agent(agent_kernel: Kernel) -> ChatCompletionAgent:
        """Create a plant management agent"""
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
                - Mention the current date when discussing watering/fertilizing schedules
                
                PLANT CARE KNOWLEDGE:
                - Ficus (Ficus elastica): Water every 1-2 weeks, fertilize monthly in growing season
                - Peace Lily (Spathiphyllum): Water when soil is dry, fertilize every 6 weeks
                - Succulents (Echeveria): Water sparingly every 2-3 weeks, fertilize quarterly
            """,
            arguments=KernelArguments(settings)
        )
        
        return agent