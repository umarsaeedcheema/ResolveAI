from fastapi import APIRouter, HTTPException
import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from config import settings, pinecone, pinecone_index
import openai
from pydantic import BaseModel

# Initialize Router
query_rag_endpoint = APIRouter()

# Initialize OpenAI Embeddings
try:
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    logging.info("OpenAI Embeddings initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize OpenAI Embeddings: {e}")
    raise HTTPException(status_code=500, detail="Failed to initialize OpenAI Embeddings.")

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
        # Step 1: Convert query to embedding
        logging.info("Generating query embedding...")
        try:
            query_embedding = embeddings.embed_query(request.query)
            logging.info(f"Query embedding generated: {query_embedding[:5]}...")  # Log snippet of the embedding
        except Exception as embedding_error:
            logging.error(f"Error generating query embedding: {embedding_error}")
            raise HTTPException(status_code=500, detail="Error generating query embedding.")

        # Step 2: Query Pinecone for relevant documents
        logging.info("Retrieving relevant documents from Pinecone...")
        try:
            response = pinecone_index.query(
                vector=query_embedding,
                top_k=3,  # Number of results to retrieve
                include_metadata=True  # Include metadata (e.g., content)
            )
            retrieved_docs = response.get('matches', [])
            if not retrieved_docs:
                logging.warning("No relevant documents found in Pinecone.")
                return QueryResponse(
                    query=request.query,
                    response="I'm sorry, I couldn't find any relevant information in the database."
                )
            logging.info(f"Retrieved {len(retrieved_docs)} documents: {retrieved_docs}")
        except Exception as retrieval_error:
            logging.error(f"Error during document retrieval from Pinecone: {retrieval_error}")
            try:
                pinecone_stats = pinecone_index.describe_index_stats()
                logging.info(f"Pinecone index stats: {pinecone_stats}")
            except Exception as stats_error:
                logging.error(f"Error fetching Pinecone index stats: {stats_error}")
            raise HTTPException(status_code=500, detail="Error retrieving documents from Pinecone.")

        # Step 3: Combine retrieved context for LLM prompt
        logging.info("Combining retrieved context...")
        try:
            context = "\n".join([doc['metadata']['content'] for doc in retrieved_docs if 'metadata' in doc and 'content' in doc['metadata']])
            if not context.strip():
                logging.warning("Retrieved documents have no valid content.")
                return QueryResponse(
                    query=request.query,
                    response="No relevant information found in the database. Please refine your query."
                )
            logging.info(f"Retrieved context: {context[:200]}...")  # Log snippet of the context
        except Exception as context_error:
            logging.error(f"Error combining retrieved context: {context_error}")
            raise HTTPException(status_code=500, detail="Error combining retrieved context.")

        # Step 4: Query the LLM with contextualized prompt
        prompt = f"Context: {context}\n\nQuestion: {request.query}\n\nAnswer:"
        logging.info(f"Generated prompt: {prompt[:200]}...")  # Log snippet of the prompt
        try:
            openai.api_key = settings.openai_api_key
            llm_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.7,
            )
            logging.info("LLM response received.")
        except Exception as llm_error:
            logging.error(f"Error during LLM query: {llm_error}")
            raise HTTPException(status_code=500, detail="Error querying the language model.")

        # Step 5: Extract response text from LLM output
        logging.info("Extracting response text from LLM output...")
        try:
            response_text = llm_response['choices'][0]['message']['content'].strip()
            logging.info(f"LLM response text: {response_text}")
            return QueryResponse(query=request.query, response=response_text)
        except Exception as parse_error:
            logging.error(f"Error parsing LLM response: {parse_error}")
            raise HTTPException(status_code=500, detail="Error parsing the LLM response.")

    except Exception as e:
        logging.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing your query: {e}")
