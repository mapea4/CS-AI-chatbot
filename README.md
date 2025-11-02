# Ursa: CS AI Chatbot

## Description

**Ursa** is an AI-powered chatbot designed to function as an academic advisor for students in the Computer Science department at Morgan State University. It uses a **Hybrid Retrieval Augmented Generation (RAG)** system to provide accurate answers. It sources information from a local knowledge base, a knowledge_base.txt file containing specific details on courses, professors, and curriculum, and from a live web search to answer general, up-to-the-minute university questions. The chatbot can understand a student's interests within a single conversation. The bot will use  conversational context to provide tailored recommendations for courses and professors. The application also features a full user authentication system (Sign Up, Login) and a ChatGPT-style chat interface that remembers your conversation history.

## Step-by-step Installation

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

# 4. Create Database & Run
# Create the local database file
flask db upgrade

# Run the application
python run.py

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

```
SENIOR PROJECT/
├── app/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── routes.py
│   ├── auth.py
│   ├── models.py
│   ├── ... (etc.)
│   └── app.db          
├── venv/
├── migrations/         
├── config.py
├── knowledge_base.txt
├── run.py
├── requirements.txt
├── .env
└── README.md
```

## Technologies Used

* **Language(s):** Python, HTML, CSS, JavaScript
* **Backend:** Flask, Flask-SQLAlchemy, Flask-Bcrypt, Flask-Login, Flask-Migrate
* **Frontend:** Tailwind CSS 
* **Database:** DQLite
* **AI & RAG:** OpenAI API (gpt-4o-mini), DDGS (DuckDuckGo Search)

## Contributing

Fork the project
1.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
2.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3.  Push to the branch (`git push origin feature/AmazingFeature`)
4.  Open a Pull Request

## 🧪 Testing

The API can be tested in two ways:

1.  **Manual Frontend Testing (Recommended):**
    * Run the server (`python run.py`).
    * Go to `http://127.0.0.1:5000` and log in.
    * Test questions and follow-up questions in the chat interface.

2.  **API Endpoint Testing (using `test.http`):**
    * Make sure your server is running.
    * In VS Code, install the "REST Client" extension.
    * Open the `test.http` file.
    * Click "Send Request" above any of the API tests.

## Known Issues

* **Knowledge Base is Manual:** The local search is only as good as the `knowledge_base.txt` file. New courses, faculty, or curriculum changes must be manually edited into the file.
* **Web Search Unreliability:** The `search_web` function relies on the `ddgs` library. It can sometimes fail to find information for time-sensitive queries (like graduation dates) if the `ddgs` service is temporarily rate-limited or can't find a good snippet.

## Future Improvements

* **Persistent User Profiles:** Create a `UserProfile` table in the database to store a user's stated interests (e.g., "AI", "Cybersecurity").
* **Proactive RAG:** Upgrade the `chatbot_service` to retrieve a user's saved interests from their profile and use *both* the chat history and the profile to find the most relevant courses.
* **"Forgot Password" Email:** Implement a real email-sending service (like Flask-Mail) for the "Forgot Password" flow.
