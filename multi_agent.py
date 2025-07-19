import os
import logging
from typing import List, Optional

from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set in environment variables.")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === AGENT COMPONENTS ===

def get_llm(model_name: str = "gpt-4") -> ChatOpenAI:
    """Returns an instance of ChatOpenAI."""
    return ChatOpenAI(
        model_name=model_name,
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY
    )

# Wikipedia Tool
wiki = WikipediaAPIWrapper()

def research_agent(query: str) -> str:
    """Uses Wikipedia API to fetch summary for a given query."""
    logger.info(f"Fetching Wikipedia info for: {query}")
    return wiki.run(query)

# Summarization Tool
def summary_agent(info: str) -> str:
    """Uses an LLM to summarize the given text."""
    prompt = PromptTemplate.from_template("Summarize this text: {text}")
    summary_prompt = prompt.format(text=info)
    llm = get_llm()
    return llm.predict(summary_prompt)

# Tool definitions
def define_tools() -> List[Tool]:
    return [
        Tool(
            name="Wikipedia Researcher",
            func=research_agent,
            description="Useful for looking up general knowledge from Wikipedia."
        ),
        Tool(
            name="Summary Agent",
            func=summary_agent,
            description="Useful for summarizing long research text or documents."
        )
    ]

# === MULTI-AGENT SYSTEM ===

def multi_agent_executor(
    query: str,
    model_name: str = "gpt-4",
    use_memory: bool = True
) -> str:
    """
    Executes the multi-agent system on a given query.
    Optionally uses conversation memory.
    """
    llm = get_llm(model_name=model_name)
    tools = define_tools()

    memory = ConversationBufferMemory(memory_key="chat_history") if use_memory else None

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory
    )

    logger.info("Running multi-agent system...")
    return agent.run(query)

# === CLI ===

def cli_interface():
    """Command-line interface for interacting with the multi-agent system."""
    print("\n🧠 SpeakMind - AI Multi-Agent System\n")
    print("Type your query or type 'exit' to quit.\n")

    while True:
        try:
            query = input(">> ")
            if query.lower() in ("exit", "quit"):
                print("Goodbye!")
                break
            response = multi_agent_executor(query)
            print(f"\n🤖 Response:\n{response}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print("An error occurred. Please try again.\n")

# === MAIN ===

if __name__ == "__main__":
    cli_interface()
