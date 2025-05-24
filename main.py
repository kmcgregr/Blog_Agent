# main.py

import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
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

def process_dream_file(file_path, llm): # Renamed function from process_dream_pdf
    """
    Processes a single dream file (PDF or TXT): extracts text, corrects it, suggests title,
    generates story, and image prompt.
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

    # Define common prompt templates (No changes needed here as they operate on extracted text)
    correction_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that corrects grammar, spelling, and improves the formatting of raw text, making it suitable for a blog post. Do not add or remove content, only refine what is provided."),
        ("user", "Please correct the following dream entry for grammar, spelling, and formatting:\n\n{dream_text}")
    ])
    correction_chain = correction_prompt | llm | StrOutputParser()

    title_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a creative content generator. Based on the following dream entry, suggest a concise and SEO-friendly title suitable for a blog post. The title should be engaging and relevant to the dream's content."),
        ("user", "Dream entry:\n\n{corrected_dream_text}\n\nSuggested SEO-friendly Title:")
    ])
    title_chain = title_prompt | llm | StrOutputParser()

    story_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a gifted storyteller. Expand the following dream entry into a creative, engaging, and slightly embellished short story. Keep it under 500 words. Use descriptive language and vivid imagery."),
        ("user", "Dream entry:\n\n{corrected_dream_text}\n\nShort Story:")
    ])
    story_chain = story_prompt | llm | StrOutputParser()

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
            "original_file": os.path.basename(file_path),
            "corrected_dream_text": corrected_dream_text.strip(),
            "seo_title": seo_title.strip().replace('\n', ' ').replace('Title:', '').strip(), # Clean up title output
            "short_story": short_story.strip(),
            "image_prompt": image_prompt.strip()
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
    llm = Ollama(model=LOCAL_LLM_MODEL)

    files_found = False
    for filename in os.listdir(INPUT_PDF_DIR): # Still using INPUT_PDF_DIR for convenience, but it now holds PDFs and TXTs
        if filename.lower().endswith((".pdf", ".txt")): # Check for both extensions
            files_found = True
            file_path = os.path.join(INPUT_PDF_DIR, filename)
            base_filename = os.path.splitext(filename)[0] # e.g., "dream_001"

            processed_data = process_dream_file(file_path, llm) # Call the renamed function
            if processed_data:
                save_processed_dream(processed_data, base_filename)
            print("-" * 40) # Separator for readability

    if not files_found:
        print(f"\nNo PDF or TXT files found in '{INPUT_PDF_DIR}'.")
        print("Please place your scanned dream PDF files or plain text dream files into this directory.")
        print("Example: Create a file named 'my_first_dream.pdf' or 'my_second_dream.txt' inside the 'input_dreams/' folder.")
    else:
        print("\nAll accessible PDF and TXT files processed. Check the 'processed_dreams/' directory for outputs.")
        print("Remember to keep `ollama serve` running in a separate terminal!")


if __name__ == "__main__":
    main()