import os
import logging
import pinecone
from pydantic import BaseSettings
from pinecone import Pinecone


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
    pc = Pinecone(
        api_key=settings.pinecone_api_key
    )
    logging.info("Pinecone client initialized successfully.")
    
     # Check if index exists
    index_name = settings.pinecone_index_name
    print(pc.list_indexes())
    if index_name not in pc.list_indexes()[0].name:
        raise ValueError(f"Pinecone index '{index_name}' does not exist in environment '{settings.pinecone_environment}'.")

    # Connect to the index
    pinecone_index = pc.Index(index_name)
    logging.info(f"Successfully connected to Pinecone index: {index_name}")

except Exception as e:
    logging.error(f"Failed to initialize Pinecone: {e}")
    raise
