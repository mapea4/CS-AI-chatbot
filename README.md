# Ursa: CS AI Chatbot

## Description

**Ursa** is an AI chatbot designed to act as an academic advisor for students in the Computer Science department at Morgan State University. It uses a **Hybrid Retrieval Augmented Generation (RAG)** system to provide accurate answers. It sources information from a local knowledge base, a knowledge_base.txt file containing specific details on courses, professors, and curriculum, and from a live web search to answer general, up-to-the-minute university questions. The chatbot can understand a student's interests within a single conversation.

## Installation

```bash
# 1. Clone the repository
git clone [your-repository-url]


# 2. Create and activate a virtual environment
# On Windows:
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install all required Python packages
pip install -r requirements.txt

# 3. Set up your Environment Variables
Find the file named .env
Open and paste your OpenAI API Key
OPENAI_API_KEY=sk-your-key-goes-here

# Run the application
python run.py
(The application will automatically create the local database after the first run)

# Access the website
Open (http://127.0.0.1:5000) in your browser.

```

## Usage

Once the server is running, you can use the application directly in your browser:
1.  **Home Page:**
    * Use the **Sign Up** button to create a new user account. This will securely hash your password and store the user in your app.db database.
    * Use the **Login** button to sign in.

2.  **Chat Page:**
    * After logging in, you will be redirected to the chat interface.
    * You can now ask the chatbot questions.


##  Project Structure

```SENIOR_PROJECT/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── chat_styles.css    # Custom styling & Dark Mode logic
│   │   ├── js/
│   │   │   ├── chat_logic.js      # Core chat & UI logic
│   │   │   └── gpa_calculator.js  # GPA calculation logic
│   │   └── images/                
│   ├── templates/
│   │   ├── index.html             # Login/Signup Landing Page
│   │   └── chat.html              # Main Application Interface
│   ├── __init__.py                # App factory & DB initialization
│   ├── routes.py                  # API endpoints & views
│   ├── auth.py                    # Authentication routes
│   ├── models.py                  # Database Schema (User, Chat)
│   ├── chatbot_service.py         # RAG Orchestrator
│   ├── prompt_builder.py          # AI System Prompt Engineering
│   ├── query_handler.py           # Local Knowledge Retriever
│   └── web_search.py              # Live Web Retriever
├── logs/                          
├── venv/                          
├── config.py                      
├── knowledge_base.txt             
├── run.py                         
├── requirements.txt              
└── .env                           # Environment variables (API Keys)
```

## Technologies Used

* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login
* **Frontend:** HTML, Tailwind CSS, JavaScript
* **Database:** SQLite
* **AI & RAG:** OpenAI API (gpt-4o-mini), DDGS (DuckDuckGo Search)

## Contributing

Fork the project
1.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
2.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3.  Push to the branch (`git push origin feature/AmazingFeature`)
4.  Open a Pull Request


## Known Issues

* **Knowledge Base is Manual:** The local search is only as good as the `knowledge_base.txt` file. New courses, faculty, or curriculum changes must be manually edited into the file.
* **Web Search Unreliability:** The `search_web` function relies on the `ddgs` library. It can sometimes fail to find information for time-sensitive queries (like graduation dates) if the `ddgs` service is temporarily rate-limited or can't find a good snippet.

## Future Improvements

* **Persistent User Profiles:** Create a `UserProfile` table in the database to store a user's stated interests (e.g., "AI", "Cybersecurity").
* **Canvas/Degree Works:** Next time, we could have integrated with the university's APIs to allow the chatbot to read a student's actual transcript and provide personalized results.
