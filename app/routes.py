from flask import Blueprint, request, jsonify, render_template  
from flask_login import login_required, current_user 
from .chatbot_service import get_answer
import logging

main_bp = Blueprint('main_bp', __name__)
logger = logging.getLogger(__name__)

# This route serves your main index.html file
@main_bp.route('/')
def index():
    return render_template('index.html') 

# --- THIS IS THE UPDATED ROUTE ---
@main_bp.route('/chat')
@login_required  # <-- 2. Add this to protect the page
def chat_page():
    # 3. Pass the logged-in user's ID to the chat.html template
    # This is the fix for the shared history bug.
    return render_template('chat.html', user_id=current_user.id)
# --- END OF UPDATE ---

@main_bp.route('/api/chat', methods=['POST'])
@login_required # <-- 4. Also protect your API route
def api_chat():
    """Handles the chat conversation from the user."""
    data = request.get_json()
    
    # We now check for 'history' (a list) instead of 'message' (a string)
    if not data or "history" not in data:
        logger.warning("Invalid request: 'history' field is required.")
        return jsonify({"error": "Invalid request: 'history' field is required."}), 400

    chat_history = data.get("history", [])
    if not chat_history or not isinstance(chat_history, list):
        logger.warning("Invalid request: 'history' must be a non-empty list.")
        return jsonify({"error": "history must be a non-empty list."}), 400

    try:
        # Log the *last* user message for context
        last_message = chat_history[-1].get("content", "NO_MESSAGE")
        logger.info(f"Received chat history. Last message: {last_message}")
        
        answer = get_answer(chat_history)
        
        return jsonify({"answer": answer})
    except Exception as e:
        logger.error(f"Error in chat API: {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred."}), 500
