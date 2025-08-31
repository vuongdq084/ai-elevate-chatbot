import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
DEPLOYMENT_NAME = "GPT-4o-mini"

# Server Configuration
HOST = "127.0.0.1"
PORT = 5000
DEBUG = False

# Database Configuration
CHROMA_DB_PATH = "./data/chroma_db"
USER_QA_COLLECTION = "user_qa"

# Audio Configuration
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "audio")

# File Paths
FRONTEND_DIR = "./web/static"
DATA_DIR = "./data"
DOCUMENTS_DIR = "./data/documents"
SCRIPTS_DIR = "./scripts"
TESTS_DIR = "./tests"
DOCS_DIR = "./docs"
