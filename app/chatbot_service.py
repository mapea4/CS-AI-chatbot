import openai
import config 
from .query_handler import load_knowledge_base, search_kb
from .web_search import search_web
from .prompt_builder import build_prompt

try:
    if not config.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in config.py")
    
    client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
    print("OpenAI client initialized successfully.")
    
except Exception as e:
    print(f"FATAL ERROR: Could not initialize OpenAI client. Details: {e}")
    print("Please make sure your 'config.py' file has a valid OPENAI_API_KEY.")
    client = None


# Load the knowledge base once when the application starts for efficiency
_KB = load_knowledge_base("knowledge_base.txt")

# --- START OF UPDATED SECTION ---

def get_answer(chat_history: list[dict]) -> str:
    """
    Orchestrates the Hybrid RAG process using the full chat history.
    """
    if not client:
        return "The chatbot AI is not configured correctly. Please check the server logs for API key errors."


    user_query = None
    for message in reversed(chat_history):
        if message['role'] == 'user':
            user_query = message['content']
            break
    
    if not user_query:
        return "I'm not sure how to respond to that. Could you ask a question?"

    
    print(f"[Orchestrator]: Searching local KB for: '{user_query}'")
    local_context = search_kb(user_query, _KB)

    
    print(f"[Orchestrator]: Searching web for: '{user_query}'")
    web_context = search_web(user_query)

    
    print("[Orchestrator]: Building prompt for AI...")
    messages = build_prompt(chat_history, local_context, web_context) 

    

    # 5. Call the OpenAI API 
    print("[Orchestrator]: Sending to OpenAI for generation...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=messages,
            temperature=0.2,      
        )
        return response.choices[0].message.content.strip()
    
    except openai.AuthenticationError:
        print("OpenAI API call failed: AuthenticationError. Your API key may be invalid or expired.")
        return "Sorry, I can't connect to the AI service right now. The API key might be incorrect."
    except Exception as e:
        print(f"An error occurred with the OpenAI API call: {e}")
        return "Sorry, I had trouble connecting to the AI service. Please try again later."
