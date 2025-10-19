# config.py

LOCAL_LLM_MODEL = "gpt-oss:20b"  # Or "mistral", "gemma", etc. - make sure you have it pulled in Ollama
INPUT_PDF_DIR = "input_dreams/" # Directory for your scanned PDF dream files
OUTPUT_DIR = "processed_dreams/" # Directory to save processed text, stories, titles, prompts

# ChromaDB is less central for *this* direct workflow, but keeping for future potential
CHROMA_DB_PATH = "chroma_db/" # Path to the ChromaDB database for potential future useex

# Prompt file paths
CORRECTION_PROMPT_FILE = "correction_prompt.xml"
TITLE_PROMPT_FILE = "title_prompt.xml"
STORY_PROMPT_FILE = "story_prompt.xml"
COPY_EDIT_PROMPT_FILE = "copy_edit_prompt.xml"
STORY_REVIEW_PROMPT_FILE = "story_review_prompt.xml"
IMAGE_PROMPT_FILE = "image_prompt_gen_prompt.xml"