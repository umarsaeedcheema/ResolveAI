# config.py
import os
import logging
import pinecone
from pydantic import BaseSettings

# Logging setup
logging.basicConfig(
    filename="data/logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.info("Logging initialized.")

# Configuration settings
class Settings(BaseSettings):
    openai_api_key: str
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index_name: str

    class Config:
        env_file = ".env"

logging.info("Loading configuration from environment variables.")
settings = Settings()
logging.info("Configuration loaded successfully.")

# Initialize Pinecone
try:
    logging.info("Initializing Pinecone client...")
    pinecone.init(
        api_key=settings.pinecone_api_key,
        environment=settings.pinecone_environment,
    )
    logging.info("Pinecone client initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Pinecone client: {e}")
