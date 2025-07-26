import streamlit as st
import requests

# Session state for conversation
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("🧠 AI Chat Assistant")

user_input = st.text_input("Type your message:")

if st.button("Send") and user_input:
    payload = {
        "message": user_input,
        "conversation_id": st.session_state.conversation_id
    }
    try:
        response = requests.post("http://localhost:5000/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.session_state.conversation_id = data.get("conversation_id")
            ai_response = data.get("ai_response")
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", ai_response))
        else:
            st.error("Error: " + response.text)
    except requests.exceptions.ConnectionError:
        st.error("Backend is not running. Please start the Flask server.")

# Display chat history
for speaker, msg in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {msg}")
