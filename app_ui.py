import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="SpeakMind – Agentic AI Chat", layout="wide")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "last_failed" not in st.session_state:
    st.session_state["last_failed"] = None
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = "You are a helpful AI assistant."

with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("Customize your assistant below:")
    st.session_state["system_prompt"] = st.text_area(
        "System Prompt", value=st.session_state["system_prompt"], height=100
    )
    st.markdown("💡 You can change the assistant behavior by editing the system prompt.")
    if st.button("🗑️ Clear Chat History"):
        st.session_state["messages"] = []
        st.experimental_rerun()

st.markdown(
    "<h1 style='text-align: center;'>🧠 SpeakMind</h1>"
    "<p style='text-align: center; font-size:17px;'>Agentic AI Chatbot powered by LangChain + LLM</p>",
    unsafe_allow_html=True,
)

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        timestamp = f"<span style='color:gray;font-size:12px;'>{message['time']}</span>"
        st.markdown(f"{message['content']}  \n\n{timestamp}", unsafe_allow_html=True)

if st.session_state["last_failed"]:
    if st.button("🔁 Retry Last Query"):
        st.chat_input = st.session_state["last_failed"]

query = st.chat_input("Type your message here...")

if query:
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state["last_failed"] = None

    with st.chat_message("user"):
        st.markdown(query)

    st.session_state["messages"].append({
        "role": "user",
        "content": query,
        "time": time_now
    })

    try:
        with st.spinner("Thinking..."):
            response = requests.get(
                f"http://127.0.0.1:9000/query",
                params={"query": query, "prompt": st.session_state["system_prompt"]},
                timeout=15
            )
            response.raise_for_status()
            ai_response = response.json().get("response", "⚠️ No response from AI.")
    except requests.exceptions.Timeout:
        ai_response = "⏱️ Request timed out. Try again."
        st.session_state["last_failed"] = query
    except Exception as e:
        ai_response = f"❌ Error: {str(e)}"
        st.session_state["last_failed"] = query

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    with st.chat_message("assistant"):
        st.markdown(ai_response)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": ai_response,
        "time": time_now
    })
