# chat.py
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv

from database import db
from models import Chat, ConversationSession
from langchain import LLMChain, PromptTemplate
from langchain.llms import GoogleGemini

load_dotenv()
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY')

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Initialize LLM chain
llm = GoogleGemini()
prompt = PromptTemplate(
    input_variables=['history', 'query'],
    template=(
        "You are a helpful e-commerce support assistant.\n"
        "Conversation so far:\n{history}\n"
        "User: {query}\n"
        "Assistant:"
    )
)
chain = LLMChain(llm=llm, prompt=prompt)

@chat_bp.route('/', methods=['POST'])
@jwt_required()
def chat():
    user_id = get_jwt_identity()
    payload = request.get_json()

    # 1) Get or create session
    conv_id = payload.get('conversation_id')
    if conv_id:
        session = ConversationSession.query.filter_by(id=conv_id, user_id=user_id).first()
        if not session:
            return jsonify(error="Invalid conversation_id"), 400
    else:
        session = ConversationSession(user_id=user_id)
        db.session.add(session)
        db.session.flush()   # to get session.id

    # 2) Build history (last 10)
    past = (
        Chat.query
            .filter_by(session_id=session.id)
            .order_by(Chat.timestamp.asc())
            .all()[-10:]
    )
    history = "\n".join(f"User: {c.message}\nAssistant: {c.response}" for c in past)

    # 3) Run LLM
    query = payload.get('query', '')
    ai_response = chain.run(history=history, query=query)

    # 4) Persist
    record = Chat(
        session_id = session.id,
        user_id    = user_id,
        message    = query,
        response   = ai_response
    )
    db.session.add(record)
    db.session.commit()

    return jsonify(conversation_id=session.id, response=ai_response), 200
