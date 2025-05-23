# Blog_Agent
AI Agent to help in my blog

Setup and How to Run:

Install Ollama: If you haven't already, download and install Ollama from ollama.com.
Pull a Model: Open your terminal and run ollama pull llama2 (or mistral, gemma, etc., depending on your preference and what you set in config.py).
Start Ollama Server: In a separate terminal window, run ollama serve. Keep this window open and running. Your Python script will connect to this local server.
Project Structure: Create a directory for your project (e.g., dream_agent/). Inside it, create:
main.py (copy the code above)
config.py (copy the code above)
requirements.txt (copy the content above)
input_dreams/ (create this empty folder)
processed_dreams/ (create this empty folder)
Place Your PDFs: Put your scanned dream PDF files into the input_dreams/ directory. For testing, you can create a simple PDF with some handwritten-like text.
Install Python Dependencies: Open a terminal, navigate to your dream_agent/ directory, and run:
Bash

pip install -r requirements.txt
Run the Agent: In the same terminal where you installed dependencies (or a new one, but not the one running ollama serve), run:
Bash

python main.py
What to Expect:

The script will check for PDFs in input_dreams/.
For each PDF, it will:
Extract text.
Send the text to your local Ollama LLM for grammar correction, title generation, story creation, and image prompt generation.
Save four output files in the processed_dreams/ directory:
[original_filename]_corrected_dream.md (containing the corrected dream text and the SEO title)
[original_filename]_short_story.md
[original_filename]_image_prompt.txt
Important Considerations & Next Steps:

PDF Quality: The quality of text extraction from scanned PDFs heavily depends on the scan quality and the clarity of handwriting. If your scans are poor, the initial text might be garbled, leading to less accurate AI outputs. Libraries like tesseract (an OCR engine) can be integrated with pypdf for better OCR, but that adds complexity and another dependency. For now, rely on pypdf's basic text extraction.
LLM Model Choice: Experiment with different Ollama models (llama2, mistral, gemma, phi3, etc.). Some might be better at creative tasks, others at correction. llama2 is a good general-purpose starting point.
Prompt Engineering: The quality of the output (especially story and image prompts) is highly dependent on the prompts given to the LLM. Feel free to tweak the ChatPromptTemplate messages to guide the LLM's behavior.
Error Handling: The current script has basic error handling for PDF loading and LLM calls. You might want to enhance it.
Batch Processing vs. Individual Processing: This script processes all PDFs in the input directory. If you want to process one by one, you'd modify the main loop.
Local Image Generation (Advanced): If you really want to generate images locally, you'd need to:
Download and run a local Stable Diffusion model (e.g., using diffusers library in Python, often requiring a strong GPU).
Integrate that model into your main.py using the generated image prompt. This is a significant step beyond the current scope and involves more dependencies and hardware. Suggesting prompts is a great, free, and hardware-light alternative.
This detailed plan and code should get you a long way to automating your dream journal! Let me know if you have specific dream entries you want to test or if you encounter any issues.