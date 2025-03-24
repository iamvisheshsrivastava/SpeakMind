import os
from together import Together
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Set your Together AI API key
TOGETHER_API_KEY = ""
client = Together(api_key=TOGETHER_API_KEY)

# Initialize memory for conversation
memory = ConversationBufferMemory()

# Define AI agent function without memory
def ai_agent(prompt):
    """Interacts with Together AI's Llama-3 model."""
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Define AI agent function with memory
def ai_agent_with_memory(prompt):
    """Interacts with Together AI with conversation memory."""
    conversation = RunnableWithMessageHistory(
        memory=memory, 
        runnable=client.chat.completions.create
    )
    return conversation.invoke(
        {"messages": [{"role": "user", "content": prompt}]}
    )["choices"][0]["message"]["content"]

# Run AI agent from terminal
if __name__ == "__main__":
    print("Choose AI Agent Mode: (1) Simple | (2) With Memory")
    mode = input("Enter 1 or 2: ").strip()

    if mode == "1":
        print("Running AI Agent (Simple)")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            response = ai_agent(user_input)
            print("Agent:", response)
    
    elif mode == "2":
        print("Running AI Agent (With Memory)")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break
            response = ai_agent_with_memory(user_input)
            print("Agent:", response)

    else:
        print("Invalid input. Please restart and choose 1 or 2.")
