from fastapi import APIRouter, HTTPException
import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from pydantic import BaseModel
from config import settings, pinecone

# Initialize Router
query_rag_endpoint = APIRouter()

# Initialize OpenAI Embeddings
try:
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    logging.info("OpenAI Embeddings initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize OpenAI Embeddings: {e}")
    raise

# Initialize Pinecone VectorStore
try:
    vector_store = Pinecone(embeddings.embed_query, settings.pinecone_index_name)
    logging.info("Pinecone VectorStore initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Pinecone VectorStore: {e}")
    raise

# Request and Response Models
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    response: str

# Query endpoint
@query_rag_endpoint.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    logging.info(f"Received query: {request.query}")
    try:
        # Convert query to embedding
        logging.info("Generating query embedding...")
        query_embedding = embeddings.embed_query(request.query)

        # Retrieve relevant documents from vector store
        logging.info("Retrieving relevant documents...")
        retrieved_docs = vector_store.similarity_search(query_embedding, top_k=3)

        if not retrieved_docs:
            logging.warning("No relevant documents found.")
            return QueryResponse(query=request.query, response="I'm sorry, I couldn't find any relevant information.")

        # Combine retrieved context for LLM prompt
        context = "\n".join([doc['content'] for doc in retrieved_docs])
        logging.info("Retrieved context prepared.")

        # Query the LLM with contextualized prompt
        prompt = f"Context: {context}\n\nQuestion: {request.query}\n\nAnswer:"
        logging.info("Querying LLM...")
        llm_response = embeddings.openai_api.create_completion(prompt=prompt, engine="gpt-3.5-turbo")

        logging.info("LLM response generated successfully.")
        return QueryResponse(query=request.query, response=llm_response['choices'][0]['text'].strip())

    except Exception as e:
        logging.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your query.")
