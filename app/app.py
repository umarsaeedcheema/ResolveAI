from fastapi import FastAPI, APIRouter
import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from config import settings, pinecone
from rag_workflow import query_rag_endpoint

# Initialize FastAPI
app = FastAPI()
logging.info("FastAPI application initialized.")
router = APIRouter()
logging.info("Router initialized.")

# Health check route
@router.get("/health-check")
def health_check():
    logging.info("Health check endpoint accessed.")
    try:
        # Test Pinecone connection
        logging.info("Testing Pinecone connection...")
        pinecone.list_indexes()
        logging.info("Pinecone connection successful.")

        # Test OpenAI API key
        logging.info("Testing OpenAI API key...")
        embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        test_embedding = embeddings.embed_query("health check")
        logging.info("OpenAI API key validation successful.")

        logging.info("All API connections are healthy.")
        return {"status": "healthy"}
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

# Add routes to the app
app.include_router(router)
app.include_router(query_rag_endpoint)
logging.info("Routes added to FastAPI application.")

if __name__ == "__main__":
    logging.info("Starting FastAPI application...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    logging.info("FastAPI application is running.")
