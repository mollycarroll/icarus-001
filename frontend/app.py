import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

st.set_page_config(page_title="Icarus the AI Resume", page_icon="🪽", layout="centered")

st.title("Icarus")
st.caption("Ask questions about Molly Carroll's experience and background")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================== SIDEBAR ==================
with st.sidebar:
    st.markdown("### Controls")
    if st.button("Clear Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()

# ================== DISPLAY CHAT HISTORY ==================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ================== USER INPUT ==================
if prompt := st.chat_input("Ask anything about Molly's background..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat", json={"question": prompt}, timeout=180
                )
                response.raise_for_status()
                answer = response.json().get(
                    "answer", "Sorry, I couldn't generate a response."
                )
            except Exception as e:
                answer = f"❌ Error connecting to backend: {str(e)}"

        message_placeholder.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
