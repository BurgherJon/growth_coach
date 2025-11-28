import os

from google.adk.agents import Agent
from google.adk.tools import google_search, FunctionTool

# Create an agent with google search tool as a search specialist
print(os.getenv('QUICK_AGENT_MODEL'))
google_search_agent = Agent(
    model=os.getenv('QUICK_AGENT_MODEL'),
    name='google_search_agent',
    description='A search agent that uses google search to get latest information about current events, weather, or business hours.',
    instruction='Use google search to answer user questions about real-time, logistical information.',
    tools=[google_search],
)

