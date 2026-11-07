# app/config.py
import os
#from list import ... # Standard imports
from dotenv import load_dotenv

# Search and load the .env file from the root directory
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

class AppConfig:
    """
    Centralized configuration engine for the ShopBuddy AI app.
    Loads values from environment matrices with safe fallbacks.
    """
    APP_NAME = "ShopBuddy AI"
    VERSION = "1.0.0-Prototype"
    
    # Environment mode toggle
    ENVIRONMENT = os.getenv("APP_ENV", "development")
    
    # --- Storage Paths ---
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CHROMA_DB_PATH = os.getenv("CUSTOM_CHROMA_DB_PATH", os.path.join(BASE_DIR, "..", "chroma_db_storage"))
    FEEDBACK_STORE_PATH = os.path.join(BASE_DIR, "..", "local_feedback.json")
    
    # --- Stripe Integrations ---
    # Pulls test or production key depending on your config settings
    MOCK_GATEWAY_ACTIVE = os.getenv("SIMULATE_PAID_GATEWAY", "false").lower() == "true"
    STRIPE_KEY = os.getenv("STRIPE_TEST_SECRET_KEY", "sk_test_mock_shopbuddy_free_tier")
    
    # --- Model Settings ---
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
    MAX_SEARCH_RESULTS = 2

config = AppConfig()
