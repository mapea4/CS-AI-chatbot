
import os
from dotenv import load_dotenv

load_dotenv()

# Example: mysql+pymysql://user:password@127.0.0.1:3306/ursa
DATABASE_URL = os.getenv("DATABASE_URL")  # optional for now

# Other knobs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ENV = os.getenv("ENV", "development")
