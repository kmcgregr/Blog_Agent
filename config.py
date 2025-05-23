# config.py

LOCAL_LLM_MODEL = "llama2"  # Or "mistral", "gemma", etc. - make sure you have it pulled in Ollama
INPUT_PDF_DIR = "input_dreams/" # Directory for your scanned PDF dream files
OUTPUT_DIR = "processed_dreams/" # Directory to save processed text, stories, titles, prompts

# ChromaDB is less central for *this* direct workflow, but keeping for future potential
CHROMA_DB_PATH = "chroma_db/" # Path to the ChromaDB database for potential future use