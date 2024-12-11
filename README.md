# Chatbot for Ooredoo customers

## Project Structure
project_root/
  |
  ├── app/
  │   ├── __init__.py         # Initialize Flask app
  │   ├── routes.py          # Define API routes
  │   ├── rag_service.py     # RAG workflow logic (retrieval and generation)
  │   ├── scraper_service.py # Data scraping logic
  │   ├── utils.py           # Helper functions
  │   ├── models/            # Embedding models and LLM integrations
  │   │   ├── __init__.py
  │   │   ├── embedding.py   # Code to generate embeddings
  │   │   ├── llm.py         # Interface with language models
  │   └── data/              # Directory for scraped and processed data
  │       ├── raw/           # Raw scraped data
  │       ├── processed/     # Cleaned and chunked data
  │       └── logs/          # Logs for monitoring
  |
  ├── streamlit_app/
  │   ├── main.py            # Streamlit UI logic
  │   ├── components.py      # Reusable UI components
  |
  ├── Dockerfile             # Docker configuration
  ├── requirements.txt       # Dependencies
  ├── .env                   # Environment variables (e.g., API keys)
  ├── .gitignore             # Git ignore file
  └── README.md              # Documentation

---