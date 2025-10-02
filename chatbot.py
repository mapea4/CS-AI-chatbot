# chatbot.py
from query_handler import load_knowledge_base, search

def main():
    kb = load_knowledge_base("knowledge_base.txt")
    print("Ursa Chatbot — Local Prototype (type 'quit' to exit)\n")
    while True:
        try:
            query = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if query.lower() in ["quit", "exit"]:
            break
        print("Bot:", search(query, kb), "\n")

if __name__ == "__main__":
    main()
