import streamlit as st
import requests

# Title
st.title("🤖 Agentic AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])

# User input
query = st.chat_input("Ask me anything...")

if query:
    st.chat_message("user").write(query)

    try:
        # Send request to backend API
        response = requests.get(f"http://127.0.0.1:9000/query?query={query}")
        response_json = response.json()

        # Get response text
        ai_response = response_json.get("response", "⚠️ Error: No response received")

    except Exception as e:
        ai_response = f"⚠️ Error: {str(e)}"

    # Show AI response
    st.chat_message("assistant").write(ai_response)

    # Save messages to session state
    st.session_state["messages"].append({"role": "user", "content": query})
    st.session_state["messages"].append({"role": "assistant", "content": ai_response})
