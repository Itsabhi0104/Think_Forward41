from flask import Blueprint, request, jsonify
import os, requests
from models.session import Session
from models.message import Message
from models.user import User
from database import db

chat_bp = Blueprint("chat_bp", __name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def call_groq_api(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", json=body, headers=headers)
    return res.json()["choices"][0]["message"]["content"]

@chat_bp.route("/", methods=["POST"])
def chat():
    data = request.get_json()
    user_id = data["user_id"]
    content = data["message"]

    # New session if not provided
    session = Session(user_id=user_id)
    db.session.add(session)
    db.session.commit()

    user_msg = Message(session_id=session.id, sender="user", content=content)
    db.session.add(user_msg)

    ai_response = call_groq_api(content)
    ai_msg = Message(session_id=session.id, sender="ai", content=ai_response)
    db.session.add(ai_msg)

    db.session.commit()

    return jsonify({
        "session_id": session.id,
        "user_message": content,
        "ai_response": ai_response
    })
