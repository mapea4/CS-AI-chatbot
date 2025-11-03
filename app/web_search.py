from ddgs import DDGS

def search_web(query: str, num_results: int = 3) -> str | None:
    """
    Performs a stable web search using the DuckDuckGo API.
    This is the reliable retriever for our RAG system.
    """
    print(f"\n[Retriever]: Searching for '{query} Morgan State University'...")
    
    search_query = f"{query} Morgan State University"
    
    try:
        # We've added timelimit='y' to get recent results (past year)
        results = DDGS().text(
            search_query, 
            backend="lite", 
            timelimit='y',  # <-- This is the important fix
            max_results=num_results
        )
        
        if not results:
            print("[Retriever]: No web search results found.")
            return None

        snippets = [r['body'] for r in results]
        
        print(f"[Retriever]: Found {len(snippets)} snippets.")
        return "\n".join([f"- {s}" for s in snippets])

    except Exception as e:
        print(f"[Retriever]: Error during web search: {e}")
        return "Could not perform web search due to an API error."
