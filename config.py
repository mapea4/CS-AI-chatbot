import os
from dotenv import dotenv_values

# Get the absolute path for the project root
basedir = os.path.abspath(os.path.dirname(__file__))

# --- Load .env file ---
dotenv_path = os.path.join(basedir, '.env')
config_values = {}
if os.path.exists(dotenv_path):
    config_values = dotenv_values(dotenv_path)
    print("Loaded environment variables directly from .env file.")
else:
    print(f"Warning: .env file not found at {dotenv_path}.")


# --- Database Configuration (NOW USING SQLITE) ---
# This creates a database file named 'app.db' inside your 'app' folder.
# It's simple, portable, and requires NO installation.
db_path = os.path.join(basedir, 'app', 'app.db')
DATABASE_URL = f"sqlite:///{db_path}"


# --- Load other variables ---
OPENAI_API_KEY = config_values.get("OPENAI_API_KEY")
if OPENAI_API_KEY:
    print(f"DEBUG: Loaded key ending in... {OPENAI_API_KEY[-4:]}")
else:
    print("WARNING in config.py: OPENAI_API_KEY is not set in your .env file.")

# Your app probably has a SECRET_KEY, let's set a default
SECRET_KEY = config_values.get("SECRET_KEY", "a-default-secret-key-for-development")

