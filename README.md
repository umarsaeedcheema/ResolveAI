# Chatbot for Ooredoo customers

## Project Structure
```
project_root/
  ├── app/
  │   ├── app.py         # Initialize FASTAPI app
  |   |-- config.py
  │   ├── routes.py           # Define API routes (to expose LangChain pipelines)
  │   ├── scraper_service.py  # Data scraping logic
  │   ├── rag_pipeline.py     # LangChain RAG logic
  │   └── data/               # Directory for scraped and processed data
  │       ├── raw/            # Raw scraped data
  │       ├── processed/      # Cleaned and chunked data
  │       └── logs/           # Logs for monitoring
  |
  ├── streamlit_app/
  │   ├── main.py             # Streamlit UI logic
  |
  ├── Dockerfile              # Docker configuration
  ├── requirements.txt        # Dependencies (include LangChain)
  ├── .env                    # Environment variables (e.g., API keys)
  ├── .gitignore              # Git ignore file
  └── README.md               # Documentation

```