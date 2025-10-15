
"""Thin wrapper around your existing KB + OpenAI logic so it can be used by Flask."""
import os
from dotenv import load_dotenv
from openai import OpenAI
from query_handler import load_knowledge_base, search

load_dotenv()

_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not _OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY missing. Set it in .env")

client = OpenAI(api_key=_OPENAI_API_KEY)

# Load KB once at import time
_KB = load_knowledge_base("knowledge_base.txt")

_SYSTEM_PROMPT = (
    "You are Ursa, an assistant for Morgan State Computer Science students. "
    "Answer accurately and concisely. If the knowledge base has relevant info, use it. "
    "If not, say what you can and suggest where a student can look on official Morgan sites."
)

def _answer_with_openai(user_query: str, context: str | None = None) -> str:
    messages = [{"role": "system", "content": _SYSTEM_PROMPT}]
    if context:
        messages.append({"role": "system", "content": f"KnowledgeBase context:\n{context}"})
    messages.append({"role": "user", "content": user_query})

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
    )
    return resp.choices[0].message.content

def get_answer(user_query: str, user_id: str | None = None) -> str:
    """Main entrypoint used by Flask.
    Attempts KB search first; includes the best match (if any) as context for OpenAI.
    """
    # Search your structured KB first; your repo's signature is search(query, kb)
    kb_hit = search(user_query, _KB)
    context = None
    if kb_hit:
        context = kb_hit if isinstance(kb_hit, str) else str(kb_hit)

    # LLM finalization step
    return _answer_with_openai(user_query, context=context)
