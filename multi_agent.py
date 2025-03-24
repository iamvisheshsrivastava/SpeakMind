from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.utilities import WikipediaAPIWrapper
from langchain.chat_models import ChatOpenAI

# Set your OpenAI API key (Use environment variables for security)
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")

# Initialize Wikipedia API Wrapper
wiki = WikipediaAPIWrapper()

def research_agent(query):
    """Fetches research information from Wikipedia."""
    return wiki.run(query)

def summary_agent(info):
    """Summarizes the given research text."""
    return ai_agent_with_memory(f"Summarize this: {info}")

# Define agent tools
tools = [
    Tool(name="Wikipedia Researcher", func=research_agent, description="Fetch research data."),
    Tool(name="Summary Agent", func=summary_agent, description="Summarize long texts."),
]

# Create the multi-agent system
def multi_agent_system(query):
    agent = initialize_agent(
        tools=tools,
        llm=ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY),
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent.run(query)

if __name__ == "__main__":
    query = input("Ask something: ")
    print(multi_agent_system(query))
