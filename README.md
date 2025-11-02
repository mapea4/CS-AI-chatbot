# Ursa The Chatbot

# Description

Ursa is an AI-powered chatbot designed to function as a 24/7 academic advisor for students in the Computer Science department at Morgan State University. It uses a Hybrid Retrieval-Augmented Generation (RAG) system to provide accurate answers. It sources information from a local knowledge base —a knowledge_base.txt file containing specific details on courses, professors, and curriculum — and from a live web search to answer general, up-to-the-minute university questions. The chatbot can understand a student's interests within a single conversation. For example, if a student says, "I am a sophomore interested in AI and cybersecurity," they can then ask, "What classes should I take?" The bot will use that conversational context to provide tailored recommendations for courses and professors. The application also features a full user authentication system (Sign Up, Login) and a ChatGPT-style chat interface that remembers your conversation history.

# Installation

This is a full-stack Flask application.

# 1. Clone the repository
git clone [your-repository-url]

# 2. Create and activate a virtual environment
# On Windows:
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# 3. Install all required Python packages
pip install -r requirements.txt

# 4. Set up your Environment Variables
#    - Create a file named .env in the root folder
#    - Add your API key and database URL. It should look like this:

OPENAI_API_KEY=sk-your-key-goes-here
DATABASE_URL=mysql+pymysql://your_db_user:your_db_pass@localhost/your_db_name

# 5. Initialize the database
#    (This assumes you are using Flask-Migrate)
flask db init
flask db migrate -m "Initial database setup"
flask db upgrade

# 6. Run the application
python run.py

# 7. Access the website
#    Open (http://127.0.0.1:5000) in your browser!


# Usage

Once the server is running, you can use the application directly in your browser:

Home Page (http://127.0.0.1:5000/):

Use the Sign Up button to create a new user account. This will securely hash your password and store the user in your MySQL database.

Use the Login button to sign in.

Chat Page (/chat):

After logging in, you will be redirected to the chat interface.

You can now ask the chatbot questions.

Chat history is saved! You can ask follow-up questions like "Who is the chair?" and then "What classes does he teach?".

The "New Chat" button in the sidebar clears the history and starts a new conversation.

# Project Structure

SENIOR PROJECT/
├── app/                  
│   ├── static/           
│   │   └── images/
│   │       ├── ursa_logo.png
│   │       └── morgan_logo.png
│   ├── templates/        
│   │   ├── index.html    
│   │   └── chat.html     
│   │
│   ├── __init__.py       
│   ├── routes.py         
│   ├── auth.py          
│   ├── models.py         
│   │
│   ├── chatbot_service.py  
│   ├── prompt_builder.py   
│   ├── query_handler.py    
│   └── web_search.py       
│
├── venv/                 
├── migrations/           
│
├── config.py             
├── knowledge_base.txt    
├── run.py               
├── requirements.txt      
├── .env                  
├── test.http             
└── README.md             


# Technologies Used

Language(s): Python, HTML, CSS, JavaScript

Backend: Flask, Flask-SQLAlchemy, Flask-Bcrypt, Flask-Login, Flask-Migrate

Frontend: Tailwind CSS (for styling)

Database: MySQL (PyMySQL driver)

AI & RAG: OpenAI API (gpt-4o-mini), DDGS (DuckDuckGo Search)


# Testing

The API can be tested in two ways:

Manual Frontend Testing (Recommended):

Run the server (python run.py).

Go to http://127.0.0.1:5000 and log in.

Test questions and follow-up questions in the /chat interface.

API Endpoint Testing (using test.http):

Make sure your server is running.

In VS Code, install the "REST Client" extension.

Open the test.http file.

Click "Send Request" above any of the API tests (e.g., TEST 2: The "Follow-up" Test).

# Known Issues

Knowledge Base is Manual: The local search is only as good as the knowledge_base.txt file. New courses, faculty, or curriculum changes must be manually edited into the file.

Web Search Unreliability: The search_web function relies on the ddgs library. It can sometimes fail to find information for time-sensitive queries (like graduation dates) if the ddgs service is temporarily rate-limited or can't find a good snippet.

# Future Improvements

Persistent User Profiles: Create a UserProfile table in the database to store a user's stated interests (e.g., "AI", "Cybersecurity").

Proactive RAG: Upgrade the chatbot_service to retrieve a user's saved interests from their profile and use both the chat history and the profile to find the most relevant courses.

"Forgot Password" Email: Implement a real email-sending service (like Flask-Mail) for the "Forgot Password" flow.
