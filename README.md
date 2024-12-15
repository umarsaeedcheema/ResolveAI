# Chatbot for Ooredoo customers

This project implements a chatbot for Ooredoo customers using Retrieval-Augmented Generation (RAG). The chatbot allows users to ask questions about uploaded documents or general information by integrating FastAPI for the backend, Streamlit for the frontend, and LangChain for the RAG pipeline. The project also uses Docker for containerization and supports deployment on AWS EC2 with a CI/CD pipeline.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Future Improvements](#future-improvements)


## Features

* Upload Documents: Admins can upload files (PDF, text, or images) to enhance the chatbot's knowledge base.
* Question Answering: Users can ask questions, and the chatbot retrieves relevant document chunks using Pinecone, generates embeddings using OpenAI, and provides context-aware answers.
* Streamlit UI: Interactive user and admin interfaces for uploading files and interacting with the chatbot.
* API-Based Backend: FastAPI endpoints for managing data and handling chatbot queries.
* Containerized Deployment: Dockerized services for backend and frontend.

## Installation
1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-directory>
```
2. Create a virtual environment
``` bash
python3 -m venv rag-bot
source rag-bot/bin/activate  # For Linux/macOS
rag-bot\Scripts\activate     # For Windows
```

3. Install Required Packages

Go into app and streamlit_ui folders and run : 
``` bash
pip install -r requirements.txt
```

4. Setup API Keys 
  1. Copy .env.example to .env
```bash
cp .env.example .env
```

  2. Add the following API Keys to the env
```bash
openai_api_key=your_openai_api_key_here
pinecone_api_key=your_pinecone_api_key_here
pinecone_environment=your_pinecone_environment_here
pinecone_index_name=your_pinecone_index_name_here
```

## Usage

1. Run Locally

Backend:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
Frontend:
```bash
streamlit run streamlit_app/main.py
```

2. Run with Docker

Build and start the containers:
```bash
docker-compose up --build
```
3. Access the services:

* Backend: http://localhost:8000

* Frontend: http://localhost:8501

## API Endpoints

1. Add Data
* Endpoint: POST /add_data
* Description: Uploads a file (PDF, text, or image) and adds its content to Pinecone after preprocessing and chunking.

2. Query Chatbot
* Endpoint: POST /query
* Description: Accepts a user query, retrieves relevant content from Pinecone, and generates a response using OpenAI GPT.

## Project Structure
```
project_root/
  ├── app/
  │   ├── app.py             # FastAPI app entry point
  │   ├── config.py          # Configuration (environment variables, API keys)
  │   ├── routes/            # API route files
  │   │   ├── add_data.py    # Endpoint for uploading and processing files
  │   │   └── rag_workflow.py# Endpoint for query handling and RAG pipeline
  │   └── logs/              # Logs for monitoring
  │   └── Dockerfile         # Dockerfile for backend
  |   └── requirements.txt   # Python dependencies
  ├── streamlit_app/
  │   ├── main.py            # Streamlit user interface
  │   └── Dockerfile         # Dockerfile for frontend
  |   └── requirements.txt   # Python dependencies
  ├── docker-compose.yml     # Docker Compose configuration for multi-service setup
  ├── .env                   # Environment variables (API keys)
  ├── .gitignore             # Ignore files for version control
  └── README.md              # Project documentation

```

## How It Works

### Document Upload:

* Admins upload files (PDFs, text, or images) via the Streamlit admin page or POST /add_data endpoint.

* Files are preprocessed, chunked, and stored in Pinecone with metadata.

### Query Handling:
* Users enter queries via the Streamlit chatbot page or POST /query endpoint.

* Pinecone retrieves relevant chunks, and OpenAI GPT generates a context-aware response.

### Frontend and Backend Communication:

* The Streamlit app interacts with the FastAPI backend using REST APIs.


## Future Improvements

* Add support for more file types.

* Enhance the admin interface with file management capabilities.

