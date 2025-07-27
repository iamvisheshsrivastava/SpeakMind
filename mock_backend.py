#!/usr/bin/env python3
"""
Mock backend for testing the SpeakMind UI improvements.
This simulates the AI agent responses without requiring API keys.
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Mock AI Agent API - Running"}

@app.get("/query/")
def ask_agent(query: str, prompt: str = "You are a helpful AI assistant."):
    # Mock response for testing
    if "error" in query.lower():
        # Simulate server error for testing error handling
        return {"error": "Simulated server error"}, 500
    
    mock_response = f"This is a mock response to: '{query}'. The backend is working correctly!"
    return {"response": mock_response}

if __name__ == "__main__":
    print("Starting mock backend server...")
    uvicorn.run(app, host="127.0.0.1", port=9000)