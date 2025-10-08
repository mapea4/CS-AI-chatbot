# query_handler.py
import re
from difflib import get_close_matches

def load_knowledge_base(file_path):
    """
    Loads the knowledge base text file into a structured dictionary.
    Each section (e.g. [COURSES], [FORMS]) becomes a dictionary key.
    """
    kb = {}
    current_section = None

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            # Detect new section headers like [COURSES]
            if line.startswith("[") and line.endswith("]"):
                current_section = line[1:-1].strip()
                kb[current_section] = []
            elif current_section:
                kb[current_section].append(line)

    return kb


def search(query, kb):
    """
    Searches through the knowledge base for the best match to the query.
    Uses fuzzy matching to find close results even if not exact.
    """
    query = query.lower().strip()
    results = []

    # Step 1: Try direct keyword detection
    section_map = {
        "course": "COURSES",
        "class": "COURSES",
        "professor": "PROFESSORS",
        "teacher": "PROFESSORS",
        "form": "FORMS",
        "curriculum": "CURRICULUM",
        "event": "EVENTS",
        "map": "MAP",
        "contact": "CONTACT INFORMATION",
        "about": "ABOUT",
    }

    section = None
    for key, val in section_map.items():
        if key in query:
            section = val
            break

    # Step 2: Search inside the chosen section
    if section and section in kb:
        data = kb[section]
        match = get_best_match(query, data)
        if match:
            return match

    # Step 3: Search across all sections if nothing found
    for section, data in kb.items():
        match = get_best_match(query, data)
        if match:
            return f"From [{section}]: {match}"

    return "Sorry, I couldn’t find an exact match for that. Try rephrasing your question."


def get_best_match(query, data):
    """
    Find the best match for the user’s query inside a list of lines.
    Returns the most relevant line of text.
    """
    matches = get_close_matches(query, data, n=1, cutoff=0.4)
    if matches:
        return matches[0]

    # Manual substring match fallback
    for line in data:
        if any(word in line.lower() for word in query.split()):
            return line
    return None
