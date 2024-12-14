from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import ChatBot
import logging
import time
from typing import List, Dict

app = FastAPI(
    title="SpeakMind - Conversational AI",
    description="An advanced conversational AI tool inspired by ChatGPT.",
    version="1.0.0",
)

chatbot = ChatBot()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    user: str
    bot: str
    timestamp: str

class AnalyticsResponse(BaseModel):
    total_requests: int
    unique_users: int
    average_response_time: float

logging.basicConfig(
    filename="speakmind.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

conversation_history: List[Dict] = []
user_analytics = {"total_requests": 0, "unique_users": set(), "total_response_time": 0}


@app.get("/")
def read_root():
    return {"message": "Welcome to SpeakMind - Conversational AI Tool"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    user_message = request.message
    if not user_message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    response = chatbot.get_response(user_message)
    response_time = time.time() - start_time

    user_analytics["total_requests"] += 1
    user_analytics["unique_users"].add("default_user")  # Simulating a unique user
    user_analytics["total_response_time"] += response_time

    chat_log = {
        "user": user_message,
        "bot": response,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    conversation_history.append(chat_log)
    logging.info(f"Chat: {chat_log}")

    return ChatResponse(**chat_log)


@app.get("/history")
def get_history():
    return {"conversation_history": conversation_history}


@app.get("/analytics", response_model=AnalyticsResponse)
def get_analytics():
    if user_analytics["total_requests"] == 0:
        avg_response_time = 0.0
    else:
        avg_response_time = user_analytics["total_response_time"] / user_analytics["total_requests"]

    analytics = {
        "total_requests": user_analytics["total_requests"],
        "unique_users": len(user_analytics["unique_users"]),
        "average_response_time": avg_response_time,
    }
    return analytics


@app.delete("/clear-history")
def clear_history():
    conversation_history.clear()
    logging.info("Conversation history cleared.")
    return {"message": "Conversation history has been cleared."}


@app.on_event("startup")
def startup_event():
    logging.info("SpeakMind server is starting up...")


@app.on_event("shutdown")
def shutdown_event():
    logging.info("SpeakMind server is shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
