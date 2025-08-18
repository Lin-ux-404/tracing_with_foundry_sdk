# Foundry Agents Tracing Demo with Frontend

This small console application to demonstrate a multi-agent system built with Semantic Kernel and Azure AI Foundry SDK for Tracing.

## Setup

1. Clone this repository
2. Create a `.env` file in the project root with the following variables:
   ```
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   MODEL_DEPLOYMENT_NAME=your_model_deployment_name
   APPLICATIONINSIGHTS_CONNECTION_STRING=your_app_insights_connection_string
   ```

3. Install the required packages:
   ```
   cd src/backend
   pip install -r requirements.txt
   ```

## Running the Application

Run the console application with this command:
```
cd src/backend
python app.py
```

Then you can start having a chat with the agent in your console. The ligs will show up in application insights and the AI Foundry UI

## Features

- Multi-agent system with orchestrator, light agent, and gardener agent
- OpenTelemetry instrumentation for tracing
- Azure Monitor integration

## Documentation
- [Azure SDK Python - Agent Telemetry Sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_telemetry/sample_agents_toolset_with_azure_monitor_tracing.py)
- [How to Trace Applications in Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/trace-application)
- [Chat Completion Agent in Semantic Kernel](https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-types/chat-completion-agent?pivots=programming-language-python)
- [Azure AI Foundry with ChatGPT](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/chatgpt)