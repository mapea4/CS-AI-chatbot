import re

SYNONYMS = {
    "cosc": ["class", "course", "computer", "science"],
    "math": ["class", "course", "math"],
    "engl": ["class", "course", "english"],
    "orns": ["class", "course"],
    "professor": ["teach", "teaches", "instructor"],
    "chair": ["chairman", "head"],
    "freshman": ["first", "year"],
    "sophomore": ["second", "year"],
    "junior": ["third", "year"],
    "senior": ["fourth", "year"],
    "graduation": ["commencement", "calendar", "academic"],
    "calendar": ["graduation", "commencement", "date", "semester"],
    "events": ["calendar", "date"]
}


CAREER_TRIGGERS = set([
    "cybersecurity", "security", "data analyst", "analytics", 
    "ai", "artificial intelligence", "machine learning", 
    "game design", "career", "recommend", "path"
])



STOP_WORDS = set([
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how", "i",
    "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was",
    "what", "when", "where", "who", "will", "with", "what's", "what is", "who is",
    "does", "the", "dr", "do", "take"
])

def load_knowledge_base(file_path: str) -> list[str]:
    """
    Loads the knowledge base text file into a flat list of lines.
    It ignores empty lines and comment lines (starting with # or [).
    """
    kb = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#") or (line.startswith("[") and line.endswith("]")):
                    continue
                kb.append(line)
    except FileNotFoundError:
        print(f"FATAL ERROR: The file '{file_path}' was not found.")
        return []
    
    print(f"[KB Loader]: Loaded {len(kb)} valid data lines from knowledge base.")
    return kb

def _normalize_text(text: str) -> set:
    """Helper function to clean text and extract enriched keywords."""
    text = re.sub(r'[^\w\s]', '', text.lower()) 
    words = set()
    
    for word in text.split():
        if word and word not in STOP_WORDS:
            
            if word.endswith('es'):
                word = word[:-2]
            elif word.endswith('s'):
                word = word[:-1]
            
            if word:
                words.add(word)
                if word in SYNONYMS:
                    words.update(SYNONYMS[word])
                
    return words

def search_kb(user_query: str, kb: list[str], threshold: int = 1) -> str | None: 
    """
    Searches the knowledge base for ALL matching lines using keyword scoring.
    A threshold of 1 is best for this bot.
    """
    if not kb:
        print("[KB Search]: Knowledge base is empty.")
        return None

    query_keywords = _normalize_text(user_query)
    found_matches = [] 
    all_course_lines = set()

    print(f"[KB Search]: Query keywords: {query_keywords}")
    
    if not query_keywords:
        print("[KB Search]: No valid keywords in query after filtering.")
        return None

    
    is_career_query = any(trigger in user_query.lower() for trigger in CAREER_TRIGGERS)
    
    if is_career_query:
        print("[KB Search]: Career query detected. Adding full course catalog to context.")

    for line in kb:
        if is_career_query:
            if line.strip().startswith("COSC") or \
               line.strip().startswith("CLCO") or \
               line.strip().startswith("MATH") or \
               line.strip().startswith("INSS") or \
               line.strip().startswith("EEGR"):
                all_course_lines.add(line)

        
        line_keywords = _normalize_text(line)
        common_keywords = query_keywords.intersection(line_keywords)
        current_score = len(common_keywords)

        if current_score >= threshold:
            found_matches.append((line, current_score, common_keywords))

    
    found_matches.sort(key=lambda x: x[1], reverse=True)
    
    final_matched_lines = [match[0] for match in found_matches]
    
    combined_context_lines = final_matched_lines + list(all_course_lines)
    final_context = "\n".join(list(dict.fromkeys(combined_context_lines)))
    
    if final_context:
        print(f"[KB Search]: Found {len(found_matches)} direct matches and {len(all_course_lines)} catalog lines.")
        return final_context
    else:
        print("[KB Search]: No local match found.")
        return None
