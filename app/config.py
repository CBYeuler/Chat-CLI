from pathlib import Path
from dotenv import load_dotenv
import os


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=BASE_DIR / '.env')

# Application settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8765))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "chat_db")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "dev-token")
MAX_HISTORY = int(os.getenv("MAX_HISTORY", 100))

#limits
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 5))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 10))
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", 500))
MAX_ROOM_NAME_LENGTH = int(os.getenv("MAX_ROOM_NAME_LENGTH", 50))
MAX_USERNAME_LENGTH = int(os.getenv("MAX_USERNAME_LENGTH", 30))
MIN_USERNAME_LENGTH = int(os.getenv("MIN_USERNAME_LENGTH", 3))
MAX_ROOMS_PER_USER = int(os.getenv("MAX_ROOMS_PER_USER", 10))
MAX_USERS_PER_ROOM = int(os.getenv("MAX_USERS_PER_ROOM", 50))

