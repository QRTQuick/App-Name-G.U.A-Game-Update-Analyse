# RAWG API Configuration
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
API_BASE_URL = "https://api.rawg.io/api"

if not RAWG_API_KEY:
    raise ValueError("RAWG_API_KEY not found in .env file")
