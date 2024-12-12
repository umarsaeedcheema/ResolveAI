import os
import json
import logging
from PyPDF2 import PdfReader

# Set up logging
logging.basicConfig(
    filename="data/logs/parser.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Directory setup
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# Function to parse PDF files
def parse_pdf(file_path):
    try:
        logging.info(f"Parsing PDF: {file_path}")
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return {"file": file_path, "content": text}
    except Exception as e:
        logging.error(f"Error parsing PDF {file_path}: {e}")
        return None

# Main function to process PDF files
def process_pdfs():
    processed_data = []

    for file_name in os.listdir(RAW_DATA_DIR):
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        if file_name.endswith(".pdf"):
            result = parse_pdf(file_path)
            if result:
                processed_data.append(result)
        else:
            logging.warning(f"Skipping non-PDF file: {file_name}")

    # Save processed data to JSON
    output_file = os.path.join(PROCESSED_DATA_DIR, "processed_pdfs.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

    logging.info(f"Processed data saved to {output_file}")

# Main entry point
if __name__ == "__main__":
    process_pdfs()