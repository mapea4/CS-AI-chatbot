import os
from openai import OpenAI
from query_handler import load_knowledge_base, search
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client (using your .env key)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    kb = load_knowledge_base("knowledge_base.txt")
    print("Ursa Chatbot — Morgan CS Assistant (type 'quit' to exit)\n")

    while True:
        try:
            query = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting Ursa. Goodbye!")
            break

        if query.lower() in ["quit", "exit"]:
            break

        # Step 1: Try to find a direct match in the knowledge base
        local_answer = search(query, kb)

        # Step 2: If found, show it directly
        if local_answer and "no match" not in local_answer.lower():
            print("Ursa:", local_answer, "\n")

        # Step 3: If not found, use OpenAI to help
        else:
            print("Ursa: Let me think...\n")
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are Ursa, an AI assistant for Morgan State Computer Science students. Be helpful and concise."},
                        {"role": "user", "content": query}
                    ]
                )
                answer = response.choices[0].message.content
                print("Ursa:", answer, "\n")

            except Exception as e:
                print("Ursa: Sorry, I ran into an issue connecting to my knowledge base or OpenAI API.")
                print("Error:", str(e), "\n")

if __name__ == "__main__":
    main()
