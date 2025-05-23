# main.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import LOCAL_LLM_MODEL, INPUT_PDF_DIR, OUTPUT_DIR

def create_output_dirs():
    """Ensures input and output directories exist."""
    os.makedirs(INPUT_PDF_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Ensured input directory: {INPUT_PDF_DIR}")
    print(f"Ensured output directory: {OUTPUT_DIR}")

def process_dream_pdf(pdf_path, llm):
    """
    Processes a single dream PDF: extracts text, corrects it, suggests title,
    generates story, and image prompt.
    """
    print(f"\n--- Processing {pdf_path} ---")
    
    # 1. Load PDF and Extract Text
    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        dream_text = "\n".join([doc.page_content for doc in documents])
        if not dream_text.strip():
            print(f"Warning: No text extracted from {pdf_path}. Skipping.")
            return None
        print("Text extracted successfully.")
    except Exception as e:
        print(f"Error loading PDF {pdf_path}: {e}")
        return None

    # Define common prompt templates
    # We use ChatPromptTemplate for better structure with Ollama models
    # It's good practice to clearly separate user and system instructions.

    # Prompt for grammar and formatting correction
    correction_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that corrects grammar, spelling, and improves the formatting of raw text, making it suitable for a blog post. Do not add or remove content, only refine what is provided."),
        ("user", "Please correct the following dream entry for grammar, spelling, and formatting:\n\n{dream_text}")
    ])
    correction_chain = correction_prompt | llm | StrOutputParser()

    # Prompt for SEO-friendly title
    title_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a creative content generator. Based on the following dream entry, suggest a concise and SEO-friendly title suitable for a blog post. The title should be engaging and relevant to the dream's content."),
        ("user", "Dream entry:\n\n{corrected_dream_text}\n\nSuggested SEO-friendly Title:")
    ])
    title_chain = title_prompt | llm | StrOutputParser()

    # Prompt for short story generation
    story_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a gifted storyteller. Expand the following dream entry into a creative, engaging, and slightly embellished short story. Keep it under 500 words. Use descriptive language and vivid imagery."),
        ("user", "Dream entry:\n\n{corrected_dream_text}\n\nShort Story:")
    ])
    story_chain = story_prompt | llm | StrOutputParser()

    # Prompt for image prompt generation
    image_prompt_gen_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI art prompt generator. Based on the following dream entry and its short story, create a detailed and imaginative text-to-image prompt suitable for an AI art model (e.g., Stable Diffusion, Midjourney). Focus on key elements, mood, and visual style. The prompt should be concise yet descriptive."),
        ("user", "Dream entry:\n\n{corrected_dream_text}\n\nShort story:\n\n{short_story}\n\nImage Generation Prompt:")
    ])
    image_prompt_gen_chain = image_prompt_gen_prompt | llm | StrOutputParser()

    # Run the chains sequentially
    try:
        print("Correcting grammar and formatting...")
        corrected_dream_text = correction_chain.invoke({"dream_text": dream_text})
        print("Generating SEO-friendly title...")
        seo_title = title_chain.invoke({"corrected_dream_text": corrected_dream_text})
        print("Generating short story...")
        short_story = story_chain.invoke({"corrected_dream_text": corrected_dream_text})
        print("Generating image prompt...")
        image_prompt = image_prompt_gen_chain.invoke({
            "corrected_dream_text": corrected_dream_text,
            "short_story": short_story
        })

        return {
            "original_pdf": os.path.basename(pdf_path),
            "corrected_dream_text": corrected_dream_text.strip(),
            "seo_title": seo_title.strip().replace('\n', ' ').replace('Title:', '').strip(), # Clean up title output
            "short_story": short_story.strip(),
            "image_prompt": image_prompt.strip()
        }
    except Exception as e:
        print(f"Error during AI processing for {pdf_path}: {e}")
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

    # Save short story
    with open(f"{output_base_name}_short_story.md", "w", encoding="utf-8") as f:
        f.write(f"## Short Story based on: {processed_data['seo_title']}\n\n")
        f.write(processed_data['short_story'])
    print(f"Saved short story to {output_base_name}_short_story.md")

    # Save image prompt
    with open(f"{output_base_name}_image_prompt.txt", "w", encoding="utf-8") as f:
        f.write(processed_data['image_prompt'])
    print(f"Saved image prompt to {output_base_name}_image_prompt.txt")

def main():
    create_output_dirs()

    # Initialize Ollama LLM
    print(f"Initializing Ollama LLM with model: {LOCAL_LLM_MODEL}")
    try:
        llm = Ollama(model=LOCAL_LLM_MODEL)
        print(f"Ollama LLM initialized successfully with model: {LOCAL_LLM_MODEL}")
    except Exception as e:
        print(f"Error initializing Ollama LLM with model '{LOCAL_LLM_MODEL}': {e}")
        print("Please ensure the model name is correct and the Ollama server is running.")
        return

    pdf_files_found = False
    for filename in os.listdir(INPUT_PDF_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_files_found = True
            pdf_path = os.path.join(INPUT_PDF_DIR, filename)
            base_filename = os.path.splitext(filename)[0] # e.g., "dream_001"

            processed_data = process_dream_pdf(pdf_path, llm)
            if processed_data:
                save_processed_dream(processed_data, base_filename)
            print("-" * 40) # Separator for readability

    if not pdf_files_found:
        print(f"\nNo PDF files found in '{INPUT_PDF_DIR}'.")
        print("Please place your scanned dream PDF files into this directory.")
        print("Example: Create a file named 'my_first_dream.pdf' inside the 'input_dreams/' folder.")
    else:
        print("\nAll accessible PDF files processed. Check the 'processed_dreams/' directory for outputs.")
        print("Remember to keep `ollama serve` running in a separate terminal!")


if __name__ == "__main__":
    main()