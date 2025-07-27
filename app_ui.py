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
        st.rerun()
    
    # Connection status check
    st.markdown("---")
    st.markdown("**Connection Status:**")
    try:
        status_response = requests.get("http://127.0.0.1:9000/", timeout=2)
        if status_response.status_code == 200:
            st.success("🟢 Backend Connected")
        else:
            st.warning("🟡 Backend Issues")
    except:
        st.error("🔴 Backend Offline")

st.markdown(
    "<h1 style='text-align: center;'>🧠 SpeakMind</h1>"
    "<p style='text-align: center; font-size:17px;'>Agentic AI Chatbot powered by LangChain + LLM</p>",
    unsafe_allow_html=True,
)

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        timestamp = f"<span style='color:gray;font-size:12px;'>{message['time']}</span>"
        st.markdown(f"{message['content']}  \n\n{timestamp}", unsafe_allow_html=True)

# Handle retry functionality - show it after messages if there's a failed query
retry_query = None
if st.session_state["last_failed"]:
    st.info(f"💡 **Last message failed**: \"{st.session_state['last_failed']}\"")
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔁 Retry", key="retry_button"):
            retry_query = st.session_state["last_failed"]
            st.session_state["last_failed"] = None
    with col2:
        if st.button("❌ Dismiss", key="dismiss_button"):
            st.session_state["last_failed"] = None
            st.rerun()

# Get user input
query = retry_query if retry_query else st.chat_input("Type your message here...")

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
        ai_response = "⏱️ **Request timed out**\n\nThe AI is taking longer than expected to respond. Please try again."
        st.session_state["last_failed"] = query
    except requests.exceptions.ConnectionError:
        ai_response = "🔌 **Connection Error**\n\nCannot connect to the AI service. Please check if the backend server is running and try again."
        st.session_state["last_failed"] = query
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            ai_response = "⚠️ **Server Error**\n\nThe AI service encountered an internal error. Please try again later."
        else:
            ai_response = f"❌ **HTTP Error**\n\nReceived error {e.response.status_code} from the AI service. Please try again."
        st.session_state["last_failed"] = query
    except Exception as e:
        # Log the full error for debugging but show user-friendly message
        error_type = type(e).__name__
        ai_response = f"❌ **Unexpected Error**\n\nSomething went wrong ({error_type}). Please try again or contact support if the problem persists."
        st.session_state["last_failed"] = query

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    with st.chat_message("assistant"):
        st.markdown(ai_response)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": ai_response,
        "time": time_now
    })
