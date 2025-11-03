def build_prompt(chat_history: list[dict], local_context: str | None, web_context: str | None) -> list:
    """
    Builds the list of messages to send to the OpenAI API, including chat history.
    This is where you define the chatbot's personality and how it should answer.
    """
    
    # 1. Start with the System Prompt (The AI's personality and rules)
    system_prompt = (
        "You are Ursa, a helpful AI assistant for Morgan State University students. "
        "Your purpose is to be a one-stop-shop for CS students. "
        "Your tone must be helpful, friendly, and professional. "
        "Formulate your final answer based *only* on the context provided below. "
        "Do not use any outside knowledge.\n\n"
        
        "--- ANSWERING RULES --- \n"
        "1.  **DO NOT COPY-PASTE:** Do not copy the context verbatim. Reformat the information into a natural, "
        "conversational answer. For example, instead of 'COSC 111 | ...', say "
        "'You will take COSC 111, which is Introduction to Computer Science I.'\n"
        
        "2.  **NEVER SHOW '|':** The context uses '|' as a separator. NEVER include the '|' character in your response. "
        "Use bullet points or natural sentences instead.\n"
        
        "3.  **ANSWER THE SPECIFIC QUESTION:** Pay close attention to the user's query. If they ask for 'freshman spring' classes, "
        "only provide the spring classes. If they ask for 'freshman' classes, provide both fall and spring.\n"
        
        "4.  **LIST 'GEN ED' OPTIONS:** If you mention 'Gen Ed', and the context provides a list of General Education options, "
        "you MUST list those options for the user.\n"
        
        "5.  **PROVIDE LINKS NATURALLY:** When you provide a link (like an RMP or Academic Calendar link), "
        "paste the full URL directly into your response. **Do not use Markdown like `[here](...)`.** "
        "For example, say: 'You can find his ratings here: https://www.ratemyprofessors.com/...' \n"
        
        "6.  **HANDLE FAILURE:** If the context does not contain the answer, clearly state that "
        "you couldn't find specific information."
    )
    
    messages = [{"role": "system", "content": system_prompt}]

    # 2. Create the RAG Context (This is "hidden" from the chat history)
    context_str = ""
    if local_context:
        context_str += f"--- Information from the Morgan State CS Department Knowledge Base ---\n{local_context}\n\n"
    if web_context:
        context_str += f"--- General Information from a Web Search ---\n{web_context}\n\n"

    if context_str:
        # Add the RAG context as a second system message
        messages.append({"role": "system", "content": f"Use the following context to answer the user's *latest* question:\n{context_str}"})
    else:
        # If no context is found, give the AI a fallback for the *latest* question
        messages.append({"role": "system", "content": "No specific information was found in our knowledge base or on the web for the user's *latest* question. Please inform the user you could not find an answer and suggest they check the official Morgan State website or rephrase their question."})

    # 3. Add the Full Chat History
    messages.extend(chat_history)
    
    return messages
