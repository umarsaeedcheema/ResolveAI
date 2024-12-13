# Chatbot for Ooredoo customers



## Installation

### Create a virtual environment

### Install the required packages

```bash
pip install -r requirements.txt
```
### API Keys 
Copy .env.example to .env

Add the following API Keys to the env

openai_api_key=your_openai_api_key_here
pinecone_api_key=your_pinecone_api_key_here
pinecone_environment=your_pinecone_environment_here
pinecone_index_name=your_pinecone_index_name_here

### Run the app 
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```




## Project Structure
```
project_root/
  ├── app/
  │   ├── app.py         # Initialize FASTAPI app
  │   ├── config.py
  │   ├── routes/             # Define API routes (to expose LangChain pipelines)
  |   |   └--add_data.py
  |   |   └--rag_workflow.py       
  │   └── data/               # Directory for scraped and processed data
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