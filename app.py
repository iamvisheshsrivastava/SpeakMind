from fastapi import FastAPI
from ai_agent import ai_agent

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Agent API"}

@app.get("/query/")
def ask_agent(query: str):
    response = ai_agent(query)
    return {"response": response}

# Run the API
# Command: uvicorn app:app --host 127.0.0.1 --port 9000 --reload
