import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

DEFAULT_MODEL = "gpt-4"
TEMPERATURE = 0.7
AGENT_MODE = "multi"
