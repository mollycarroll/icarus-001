import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
HF_TOKEN = os.getenv("HF_TOKEN")
