from flask import Blueprint, request, jsonify, render_template  
from flask_login import login_required, current_user 
from .chatbot_service import get_answer
import logging
import re
import datetime

main_bp = Blueprint('main_bp', __name__)
logger = logging.getLogger(__name__)

@main_bp.route('/')
def index():
    return render_template('index.html') 

@main_bp.route('/chat')
@login_required 
def chat_page():
    return render_template('chat.html', user_id=current_user.id)

@main_bp.route('/api/upcoming_deadlines')
@login_required
def get_upcoming_deadlines():
    """
    Scans the knowledge_base.txt for any academic calendar dates
    that are between today and the next 14 days.
    """
    upcoming_deadlines = []
    try:
        today = datetime.date.today()
        two_weeks_from_today = today + datetime.timedelta(days=14)
        
        in_calendar_section = False
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            for line in f:
                
                if line.strip().startswith("[ACADEMIC_CALENDAR_FALL_2025]"):
                    in_calendar_section = True
                    continue

                
                if in_calendar_section and line.strip().startswith("["):
                    break
                
                if in_calendar_section and "|" in line:
                    
                    parts = line.split("|", 1)
                    if len(parts) == 2:
                        raw_date_part = parts[0].strip().replace("Date:", "").strip()
                        event_part = parts[1].strip().replace("Event:", "").strip()

                        
                        match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", raw_date_part)
                        if match:
                            start_date_str = match.group(1)
                            try:
                                deadline_date = datetime.datetime.strptime(start_date_str, "%m/%d/%Y").date()
                                
                                
                                if today <= deadline_date <= two_weeks_from_today:
                                    
                                    upcoming_deadlines.append(f"<strong>{raw_date_part}:</strong> {event_part}")
                            except ValueError:
                                continue
                            
    except Exception as e:
        logger.error(f"Error fetching upcoming deadlines: {e}", exc_info=True)
        return jsonify({"deadlines": []})

    return jsonify({"deadlines": upcoming_deadlines})


@main_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """Handles the chat conversation from the user."""
    data = request.get_json()
    
    if not data or "history" not in data:
        logger.warning("Invalid request: 'history' field is required.")
        return jsonify({"error": "Invalid request: 'history' field is required."}), 400

    chat_history = data.get("history", [])
    if not chat_history or not isinstance(chat_history, list):
        logger.warning("Invalid request: 'history' must be a non-empty list.")
        return jsonify({"error": "history must be a non-empty list."}), 400

    try:
        last_message = chat_history[-1].get("content", "NO_MESSAGE")
        logger.info(f"Received chat history. Last message: {last_message}")
        
        answer = get_answer(chat_history)
        
        return jsonify({"answer": answer})
    except Exception as e:
        logger.error(f"Error in chat API: {e}", exc_info=True)
        return jsonify({"error": "An internal server error occurred."}), 500
