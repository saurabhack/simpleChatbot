import os
import streamlit as st
from openai import OpenAI
# 1. Connect to Ollama Cloud instead of localhost
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GSK_API_KEY"],
)
st.title("My Cloud AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, concise assistant."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="qwen/qwen3.8-27b",  # Use a supported Ollama Cloud model
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})