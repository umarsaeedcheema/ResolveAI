from fastapi import APIRouter, HTTPException, UploadFile, File
import logging
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pytesseract
from config import settings, pinecone
import os

# Initialize Router
add_data_endpoint = APIRouter()

# Initialize OpenAI Embeddings
try:
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    logging.info("OpenAI Embeddings initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize OpenAI Embeddings: {e}")
    raise

# Initialize Pinecone VectorStore
try:
    vector_store = Pinecone(embeddings.embed_query, settings.pinecone_index_name, text_key="content")
    logging.info("Pinecone VectorStore initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize Pinecone VectorStore: {e}")
    raise

# Helper functions for semantic chunking
def parse_and_chunk_pdf(file_path):
    logging.info(f"Parsing and chunking PDF: {file_path}")
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    return [{"content": chunk, "file": file_path} for chunk in chunks]

def parse_and_chunk_text(content):
    logging.info("Parsing and chunking text file...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(content.decode("utf-8"))
    return [{"content": chunk, "file": "uploaded_text.txt"} for chunk in chunks]

def parse_and_chunk_image(file_path):
    logging.info(f"Parsing and chunking image: {file_path}")
    text = pytesseract.image_to_string(Image.open(file_path))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    return [{"content": chunk, "file": file_path} for chunk in chunks]

# Generic endpoint to add data to Pinecone
@add_data_endpoint.post("/add-data")
def add_data_to_pinecone(file: UploadFile = File(...)):
    try:
        logging.info(f"Uploading and processing file: {file.filename}")
        # Determine file type
        file_extension = os.path.splitext(file.filename)[1].lower()

        # Read file content
        content = file.file.read()
        temp_path = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)

        with open(temp_path, "wb") as temp_file:
            temp_file.write(content)

        # Process based on file type
        if file_extension in [".pdf"]:
            parsed_content = parse_and_chunk_pdf(temp_path)
        elif file_extension in [".txt"]:
            parsed_content = parse_and_chunk_text(content)
        elif file_extension in [".jpg", ".png"]:
            parsed_content = parse_and_chunk_image(temp_path)
        else:
            logging.warning("Unsupported file type.")
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        # Add parsed content to Pinecone
        for chunk in parsed_content:
            vector_store.add_texts([chunk["content"]], metadata={"file": chunk["file"]})
            logging.info(f"Added content from {chunk['file']} to Pinecone.")

        # Clean up temporary file
        os.remove(temp_path)

        return {"status": "success", "message": f"File {file.filename} processed and added to Pinecone."}

    except Exception as e:
        logging.error(f"Error adding data to Pinecone: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the file.")
