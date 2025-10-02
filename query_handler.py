# query_handler.py
# Local query handling (no API keys). Intent routing + fuzzy matching + synonyms.
from difflib import get_close_matches
import re

SECTION_HEADERS = {"COURSES", "FORMS", "CURRICULUM GUIDE"}

SYNONYMS = {
    "data structures": "CSCI 241",
    "operating systems": "CSCI 351",
    "computer organization": "CSCI 254",
    "intro to cs": "CSCI 111",
    "intermediate programming": "CSCI 112",
    "max credit": "Maximum Credit Form",
    "maximum credit": "Maximum Credit Form",
    "override": "Prerequisite Override Form",
    "prereq override": "Prerequisite Override Form",
    "curriculum guide": "CURRICULUM GUIDE",
}

INTENT_KEYWORDS = {
    "COURSES": ["course help", "courses", "class", "classes", "csci"],
    "FORMS": ["form", "forms", "override", "maximum credit", "independent study"],
    "CURRICULUM GUIDE": ["curriculum", "guide", "plan", "sequence"],
}

def load_knowledge_base(path="knowledge_base.txt"):
    kb = {}
    section = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].upper()
                kb[section] = []
            elif section:
                kb[section].append(line)
    return kb

def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

def guess_intent(query):
    qn = normalize(query)
    for section, kws in INTENT_KEYWORDS.items():
        if any(kw in qn for kw in kws):
            return section
    for key, val in SYNONYMS.items():
        if key in qn:
            return "FORMS" if "form" in val.lower() else "COURSES"
    return "COURSES"

def search(query, kb):
    intent = guess_intent(query)
    results = kb.get(intent, [])
    if not results:
        return "Sorry, I couldn't find anything."
    match = get_close_matches(query, results, n=1, cutoff=0.4)
    if match:
        return f"{intent} match: {match[0]}"
    return f"{intent} info: " + ", ".join(results)
