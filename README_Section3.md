
# Section 3 — Web Server + API

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env  # then edit values
python app.py
```

- API base: `http://localhost:5000`
- Health: `GET /health`
- Chat: `POST /api/chat` with JSON `{"message": "your question"}`

## Example1
```bash
curl -X POST http://localhost:5000/api/chat   -H "Content-Type: application/json"   -d '{"message": "Where can I find the Maximum Credit Form?"}'
```

## Small Notes
- Uses your existing `knowledge_base.txt` and `query_handler.py`.
- Logging goes to `logs/app.log` (created at runtime).
- DB is optional; set `DATABASE_URL` if available (MySQL). See `bootstrap.sql`.
- For production: `gunicorn -w 2 -b 0.0.0.0:5000 app:app`
```

### If your repo already has `requirements.txt`
Add (or verify) these lines are present:
```
flask
flask-cors
python-dotenv
openai>=1.30.0
SQLAlchemy>=2.0
PyMySQL
```
