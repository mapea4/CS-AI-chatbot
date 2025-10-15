
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.exceptions import BadRequest
from chatbot_service import get_answer
from db import get_engine

app = Flask(__name__)
CORS(app)

# --- Logging ---
handler = RotatingFileHandler("logs/app.log", maxBytes=1_000_000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

@app.route("/health", methods=["GET"])
def health():
    """Healthcheck: API up + optional DB ping."""
    payload = {"status": "ok"}
    try:
        engine = get_engine(optional=True)
        if engine is not None:
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            payload["db"] = "ok"
        return jsonify(payload), 200
    except Exception as e:
        app.logger.exception("/health failure")
        return jsonify({"status": "degraded", "error": str(e)}), 503

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Accepts JSON: {"message": "...", "user_id": "optional"} and returns {"answer": "..."}"""
    if not request.is_json:
        raise BadRequest("Content-Type must be application/json")

    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    user_id = data.get("user_id")  # optional, for personalization later

    if not message:
        raise BadRequest("Field 'message' is required and cannot be empty.")

    try:
        answer = get_answer(message, user_id=user_id)
        return jsonify({"answer": answer}), 200
    except Exception as e:
        app.logger.exception("/api/chat error")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == "__main__":
    # For local dev; in production use gunicorn/uwsgi
    app.run(host="0.0.0.0", port=5000, debug=True)
