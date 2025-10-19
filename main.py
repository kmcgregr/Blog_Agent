
# main.py

import os
import argparse
import xml.etree.ElementTree as ET
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import (
    LOCAL_LLM_MODEL, INPUT_PDF_DIR, OUTPUT_DIR,
    CORRECTION_PROMPT_FILE, TITLE_PROMPT_FILE, STORY_PROMPT_FILE,
    COPY_EDIT_PROMPT_FILE, STORY_REVIEW_PROMPT_FILE, IMAGE_PROMPT_FILE
)

def create_output_dirs():
    """Ensures input and output directories exist."""
    os.makedirs(INPUT_PDF_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Ensured input directory: {INPUT_PDF_DIR}")
    print(f"Ensured output directory: {OUTPUT_DIR}")

def load_prompt_from_xml(file_path):
    """Loads a prompt from an XML file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        system_message = root.find('system').text.strip()
        user_message = root.find('user').text.strip()
        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("user", user_message)
        ])
    except Exception as e:
        print(f"Error loading prompt from {file_path}: {e}")
        return None

def process_dream_file(file_path, llm):
    """
    Processes a single dream file (PDF or TXT): extracts text, corrects it, suggests title,
    generates story, copy-edits the story, and creates an image prompt.
    """
    print(f"\n--- Processing {file_path} ---")

    # 1. Load File and Extract Text
    dream_text = ""
    try:
        if file_path.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            dream_text = "\n".join([doc.page_content for doc in documents])
            print(f"Text extracted from PDF: {file_path}")
        elif file_path.lower().endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
            documents = loader.load()
            dream_text = "\n".join([doc.page_content for doc in documents])
            print(f"Text extracted from TXT: {file_path}")
        else:
            print(f"Skipping unsupported file type: {file_path}")
            return None

        if not dream_text.strip():
            print(f"Warning: No text extracted or text is empty from {file_path}. Skipping.")
            return None
    except Exception as e:
        print(f"Error loading file {file_path}: {e}")
        return None

    # Load prompts from external files
    correction_prompt = load_prompt_from_xml(CORRECTION_PROMPT_FILE)
    title_prompt = load_prompt_from_xml(TITLE_PROMPT_FILE)
    story_prompt = load_prompt_from_xml(STORY_PROMPT_FILE)
    copy_edit_prompt = load_prompt_from_xml(COPY_EDIT_PROMPT_FILE)
    story_review_prompt = load_prompt_from_xml(STORY_REVIEW_PROMPT_FILE)
    # image_prompt_gen_prompt = load_prompt_from_xml(IMAGE_PROMPT_FILE)

    if not all([correction_prompt, title_prompt, story_prompt, copy_edit_prompt, story_review_prompt]):
        print("One or more prompts could not be loaded. Aborting.")
        return None

    # Define chains
    correction_chain = correction_prompt | llm | StrOutputParser()
    title_chain = title_prompt | llm | StrOutputParser()
    story_chain = story_prompt | llm | StrOutputParser()
    copy_edit_chain = copy_edit_prompt | llm | StrOutputParser()
    story_review_chain = story_review_prompt | llm | StrOutputParser()
    # image_prompt_gen_chain = image_prompt_gen_prompt | llm | StrOutputParser()

    # Run the chains sequentially
    try:
        print("Correcting grammar and formatting...")
        corrected_dream_text = correction_chain.invoke({"dream_text": dream_text})
        print("Generating SEO-friendly title...")
        seo_title = title_chain.invoke({"corrected_dream_text": corrected_dream_text})
        print("Generating short story...")
        short_story_draft = story_chain.invoke({"corrected_dream_text": corrected_dream_text})
        print("Copy-editing the short story...")
        final_short_story = copy_edit_chain.invoke({"short_story": short_story_draft})
        print("Reviewing the short story...")
        reviewed_story = story_review_chain.invoke({"final_short_story": final_short_story})
        # print("Generating image prompt...")
        # image_prompt = image_prompt_gen_chain.invoke({
        #     "corrected_dream_text": corrected_dream_text,
        #     "short_story": final_short_story
        # })

        return {
            "original_file": os.path.basename(file_path),
            "corrected_dream_text": corrected_dream_text.strip(),
            "seo_title": seo_title.strip().replace('\n', ' ').replace('Title:', '').strip(),
            "short_story_draft": short_story_draft.strip(),
            "final_short_story": final_short_story.strip(),
            "reviewed_story": reviewed_story.strip(),
            # "image_prompt": image_prompt.strip()
        }
    except Exception as e:
        print(f"Error during AI processing for {file_path}: {e}")
        print("Please ensure your Ollama server is running and the model is downloaded.")
        return None

def save_processed_dream(processed_data, base_filename):
    """Saves the processed dream data into separate files."""
    if not processed_data:
        return

    output_base_name = os.path.join(OUTPUT_DIR, base_filename)

    # Save corrected dream text
    with open(f"{output_base_name}_corrected_dream.md", "w", encoding="utf-8") as f:
        f.write(f"# {processed_data['seo_title']}\n\n")
        f.write(processed_data['corrected_dream_text'])
    print(f"Saved corrected dream and title to {output_base_name}_corrected_dream.md")

    # Save initial story draft
    with open(f"{output_base_name}_story_draft.md", "w", encoding="utf-8") as f:
        f.write(f"## Initial Story Draft for: {processed_data['seo_title']}\n\n")
        f.write(processed_data['short_story_draft'])
    print(f"Saved initial story draft to {output_base_name}_story_draft.md")

    # Save final (copy-edited) short story
    with open(f"{output_base_name}_final_short_story.md", "w", encoding="utf-8") as f:
        f.write(f"## Final (Copy-Edited) Story for: {processed_data['seo_title']}\n\n")
        f.write(processed_data['final_short_story'])
    print(f"Saved final short story to {output_base_name}_final_short_story.md")

    # Save reviewed story
    with open(f"{output_base_name}_reviewed_story.md", "w", encoding="utf-8") as f:
        f.write(f"## Reviewed Story for: {processed_data['seo_title']}\n\n")
        f.write(processed_data['reviewed_story'])
    print(f"Saved reviewed story to {output_base_name}_reviewed_story.md")

    # Save image prompt
    # with open(f"{output_base_name}_image_prompt.txt", "w", encoding="utf-8") as f:
    #     f.write(processed_data['image_prompt'])
    # print(f"Saved image prompt to {output_base_name}_image_prompt.txt")

def main():
    parser = argparse.ArgumentParser(description="Process dream files into blog content.")
    parser.add_argument("--model", default=LOCAL_LLM_MODEL,
                        help=f"The Ollama model to use (default: {LOCAL_LLM_MODEL})")
    args = parser.parse_args()

    create_output_dirs()

    # Initialize Ollama LLM
    print(f"Initializing Ollama LLM with model: {args.model}")
    llm = Ollama(model=args.model)

    files_found = False
    for filename in os.listdir(INPUT_PDF_DIR):
        if filename.lower().endswith((".pdf", ".txt")):
            files_found = True
            file_path = os.path.join(INPUT_PDF_DIR, filename)
            base_filename = os.path.splitext(filename)[0]

            processed_data = process_dream_file(file_path, llm)
            if processed_data:
                save_processed_dream(processed_data, base_filename)
            print("-" * 40)

    if not files_found:
        print(f"\nNo PDF or TXT files found in '{INPUT_PDF_DIR}'.")
        print("Please place your scanned dream PDF files or plain text dream files into this directory.")
        print("Example: Create a file named 'my_first_dream.pdf' or 'my_second_dream.txt' inside the 'input_dreams/' folder.")
    else:
        print("\nAll accessible PDF and TXT files processed. Check the 'processed_dreams/' directory for outputs.")
        print("Remember to keep `ollama serve` running in a separate terminal!")


if __name__ == "__main__":
    main()
