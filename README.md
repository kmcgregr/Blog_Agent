# Dream Journal Agent

An AI-powered agent that transforms dream journal entries into polished blog content using LangChain and Ollama.

## Features

- 📝 **Automatic Grammar Correction**: Cleans up and formats raw dream text
- 🎯 **SEO Title Generation**: Creates engaging, search-friendly titles
- 📖 **Story Generation**: Transforms dreams into compelling 7-chapter narratives
- ✍️ **Copy Editing**: Professional editing for publication-ready content
- 🔍 **Story Review**: Expert literary analysis and feedback
- 🎨 **Image Prompts**: Generates AI art prompts based on dream content

## Architecture

This project uses a modular, agent-based architecture with LangChain:

- **Agent Pattern**: `DreamAgent` orchestrates all processing
- **Chain Pattern**: Separate chains for each processing step
- **Loader Pattern**: Extensible document loading system
- **Writer Pattern**: Flexible output formatting

## Installation

### Prerequisites

1. **Install Ollama**: Download from [ollama.com](https://ollama.com)
2. **Pull a Model**: 
   ```bash
   ollama pull llama2
   # or
   ollama pull mistral
   ```
3. **Start Ollama Server**: 
   ```bash
   ollama serve
   ```

### Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd dream_agent
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create directory structure**:
   ```bash
   mkdir -p input_dreams processed_dreams prompts
   ```

5. **Move prompt files** to `prompts/` directory:
   ```bash
   mv *.xml prompts/
   ```

## Project Structure

```
dream_agent/
├── main.py                     # Entry point
├── config.py                   # Configuration
├── agents/
│   └── dream_agent.py         # Main orchestrator
├── chains/
│   └── processing_chains.py   # LangChain chains
├── loaders/
│   └── document_loader.py     # Document loading
├── processors/
│   └── dream_processor.py     # Processing pipeline
├── writers/
│   └── output_writer.py       # Output generation
├── utils/
│   └── prompt_loader.py       # Prompt utilities
├── prompts/                    # XML prompt templates
├── input_dreams/               # Input files (PDF/TXT)
└── processed_dreams/           # Output files
```

## Usage

### Basic Usage

Process all files in `input_dreams/`:
```bash
python main.py
```

### Command Line Options

```bash
# Use a different model
python main.py --model mistral

# Process a single file
python main.py --file input_dreams/my_dream.pdf

# Custom input/output directories
python main.py --input my_dreams/ --output blog_posts/

# Adjust temperature for creativity
python main.py --temperature 0.8

# Enable verbose logging
python main.py --verbose
```

### Full Example

```bash
# 1. Start Ollama (in separate terminal)
ollama serve

# 2. Place your dream files
cp my_dream.pdf input_dreams/

# 3. Run the agent
python main.py --model mistral --verbose

# 4. Check outputs
ls processed_dreams/
```

## Configuration

Edit `config.py` to customize:

```python
class Config(BaseModel):
    # LLM Settings
    llm_model: str = "gpt-oss:20b"
    llm_temperature: float = 0.7
    
    # Directories
    input_pdf_dir: Path = Path("input_dreams/")
    output_dir: Path = Path("processed_dreams/")
    
    # Processing
    max_retries: int = 3
    timeout: int = 300
```

## Output Files

For each input file, the agent generates:

1. **`*_corrected_dream.md`**: Cleaned and formatted dream text with title
2. **`*_story_draft.md`**: Initial 7-chapter story
3. **`*_final_short_story.md`**: Copy-edited version
4. **`*_reviewed_story.md`**: Literary review and feedback
5. **`*_image_prompt.txt`**: AI art generation prompt

## Extending the Agent

### Add a New Processing Step

1. **Create a new prompt** in `prompts/`:
   ```xml
   <prompt>
       <system>Your system instructions</system>
       <user>Your user template with {variables}</user>
   </prompt>
   ```

2. **Add to config.py**:
   ```python
   my_new_prompt_file: str = "my_prompt.xml"
   ```

3. **Add chain in `processing_chains.py`**:
   ```python
   def process_my_step(self, input_text: str) -> Optional[str]:
       if self.my_chain is None:
           return None
       return self.my_chain.invoke({"input_text": input_text})
   ```

4. **Update `dream_processor.py`** to include the step

### Add a New Document Type

Extend `DocumentLoader` in `loaders/document_loader.py`:

```python
@staticmethod
def _load_docx(file_path: Path) -> Optional[str]:
    # Your loading logic
    pass
```

## Troubleshooting

### Ollama Connection Error

```
Error: Failed to connect to Ollama
```

**Solution**: Ensure Ollama is running:
```bash
ollama serve
```

### Model Not Found

```
Error: Model 'xyz' not found
```

**Solution**: Pull the model:
```bash
ollama pull xyz
```

### Empty Output

**Solution**: Check logs for errors:
```bash
python main.py --verbose
```

### Import Errors

**Solution**: Ensure all `__init__.py` files exist:
```bash
touch agents/__init__.py chains/__init__.py loaders/__init__.py \
      processors/__init__.py writers/__init__.py utils/__init__.py
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
# Format code
black .

# Check types
mypy .

# Lint
flake8 .
```

### Adding Logging

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Info message")
logger.error("Error message")
```

## Performance Tips

1. **Use faster models** for drafts: `ollama pull phi3`
2. **Batch processing**: Process multiple files at once
3. **Adjust temperature**: Lower = more consistent, Higher = more creative
4. **GPU acceleration**: Ensure Ollama uses your GPU

## Future Enhancements

- [ ] Async processing for better performance
- [ ] Web interface using Streamlit
- [ ] Support for DOCX, HTML formats
- [ ] Vector database integration for dream similarity
- [ ] Multi-language support
- [ ] Custom style templates
- [ ] Scheduled batch processing
- [ ] Cloud deployment options

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Powered by [Ollama](https://ollama.com/)
- Inspired by dream journaling practices

## Support

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Documentation**: See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

**Note**: Remember to keep `ollama serve` running in a separate terminal while using this agent!