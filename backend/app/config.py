import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
HF_MODEL = os.getenv("HF_MODEL", "google/gemma-3-4b-it")
HF_TOKEN = os.getenv("HF_TOKEN")
