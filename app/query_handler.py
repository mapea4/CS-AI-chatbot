import re

# This is our new "synonym" dictionary to make the search smarter
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
    # --- NEW SYNONYMS ---
    "graduation": ["commencement", "calendar", "academic"],
    "calendar": ["graduation", "commencement", "date", "semester"],
    "events": ["calendar", "date"]
}

# A much smaller, safer list of "fluff" words to ignore
STOP_WORDS = set([
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how", "i",
    "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was",
    "what", "when", "where", "who", "will", "with", "what's", "what is", "who is",
    "does", "the", "dr"
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
                # Ignore empty, comment, or section-header lines
                if not line or line.startswith("#") or (line.startswith("[") and line.endswith("]")):
                    continue
                
                # Add the valid data line to our list
                kb.append(line)
    except FileNotFoundError:
        print(f"FATAL ERROR: The file '{file_path}' was not found.")
        return []
    
    print(f"[KB Loader]: Loaded {len(kb)} valid data lines from knowledge base.")
    return kb

def _normalize_text(text: str) -> set:
    """Helper function to clean text and extract enriched keywords."""
    text = re.sub(r'[^\w\s]', '', text.lower()) # Keep numbers (like 470)
    words = set()
    
    for word in text.split():
        if word and word not in STOP_WORDS:
            # Simple stemming: remove 's' and 'es'
            if word.endswith('es'):
                word = word[:-2]
            elif word.endswith('s'):
                word = word[:-1]
            
            if word:
                words.add(word)
                
                # --- THIS IS THE NEW LOGIC ---
                # If the word has synonyms, add them to the set
                if word in SYNONYMS:
                    words.update(SYNONYMS[word])
                # --- END NEW LOGIC ---
                
    return words

# --- THIS IS THE UPDATED FUNCTION DEFINITION ---
def search_kb(user_query: str, kb: list[str], threshold: int = 2) -> str | None:
    """
    Searches the knowledge base for ALL matching lines using keyword scoring.
    Default threshold is now 2 to prevent weak matches.
    """
    if not kb:
        print("[KB Search]: Knowledge base is empty.")
        return None

    query_keywords = _normalize_text(user_query)
    found_matches = [] # We now collect a list of all good matches

    print(f"[KB Search]: Query keywords: {query_keywords}")
    
    if not query_keywords:
        print("[KB Search]: No valid keywords in query after filtering.")
        return None

    for line in kb:
        line_keywords = _normalize_text(line)
        
        # Calculate score based on number of matching keywords
        common_keywords = query_keywords.intersection(line_keywords)
        current_score = len(common_keywords)

        # If the line meets our minimum score, add it to the list
        if current_score >= threshold:
            # We will store the line and its score
            found_matches.append((line, current_score, common_keywords))

    # Sort matches by score (highest first) to put the most relevant context first
    found_matches.sort(key=lambda x: x[1], reverse=True)
    
    # Now, join all found lines into one big context string
    if found_matches:
        # We just want the text, not the score
        final_lines = [match[0] for match in found_matches]
        combined_context = "\n".join(final_lines)
        
        print(f"[KB Search]: Found {len(found_matches)} matching lines. Top match keywords: {found_matches[0][2]}")
        return combined_context
    else:
        print("[KB Search]: No local match found above threshold.")
        return None
