# RAWG API Configuration
import os
import logging
from dotenv import load_dotenv, find_dotenv

# Attempt to locate a .env file; if found, load it. Otherwise rely on the
# environment (CI, production, or user-run). This prevents hard failures
# during CI builds when a local .env is intentionally absent.
dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path)

# Read from the environment (after loading .env if present).
RAWG_API_KEY = os.environ.get("RAWG_API_KEY")
API_BASE_URL = "https://api.rawg.io/api"

if not RAWG_API_KEY:
    logging.warning(
        "RAWG_API_KEY is not set. API requests that require a key may fail."
    )
