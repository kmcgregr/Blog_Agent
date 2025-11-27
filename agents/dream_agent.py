# agents/dream_agent.py
from pathlib import Path
from typing import Optional
from langchain_community.llms import Ollama
from config import Config
from utils.prompt_loader import PromptLoader
from chains.processing_chains import ProcessingChains
from processors.dream_processor import DreamProcessor
from writers.output_writer import OutputWriter
import logging

logger = logging.getLogger(__name__)

class DreamAgent:
    """Main agent orchestrating the dream processing pipeline"""
    
    def __init__(self, config: Config):
        """
        Initialize the Dream Agent.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.llm: Optional[Ollama] = None
        self.processing_chains: Optional[ProcessingChains] = None
        self.processor: Optional[DreamProcessor] = None
        self.writer: Optional[OutputWriter] = None
        
        # Initialize components
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize all components of the agent"""
        logger.info("Initializing Dream Agent...")
        
        # Ensure directories exist
        self.config.ensure_directories()
        
        # Initialize LLM
        self._init_llm()
        
        # Load prompts
        prompts = self._load_prompts()
        
        # Initialize processing chains
        if self.llm and prompts:
            self.processing_chains = ProcessingChains(self.llm, prompts)
            self.processor = DreamProcessor(self.processing_chains)
            self.writer = OutputWriter(self.config.output_dir)
            logger.info("Dream Agent initialized successfully")
        else:
            logger.error("Failed to initialize Dream Agent")
    
    def _init_llm(self) -> None:
        """Initialize the Ollama LLM"""
        try:
            logger.info(f"Connecting to Ollama with model: {self.config.llm_model}")
            self.llm = Ollama(
                model=self.config.llm_model,
                temperature=self.config.llm_temperature,
                base_url=self.config.llm_base_url
            )
            logger.info("✓ Ollama LLM initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama LLM: {e}")
            logger.error("Please ensure Ollama is running with: ollama serve")
            self.llm = None
    
    def _load_prompts(self) -> dict:
        """Load all prompt templates"""
        logger.info("Loading prompt templates...")
        
        prompt_files = {
            'correction': self.config.get_prompt_path(self.config.correction_prompt_file),
            'title': self.config.get_prompt_path(self.config.title_prompt_file),
            'story': self.config.get_prompt_path(self.config.story_prompt_file),
            'copy_edit': self.config.get_prompt_path(self.config.copy_edit_prompt_file),
            'review': self.config.get_prompt_path(self.config.story_review_prompt_file),
            'image_prompt': self.config.get_prompt_path(self.config.image_prompt_file)
        }
        
        prompts = PromptLoader.load_multiple(prompt_files)
        
        # Check if all prompts loaded successfully
        loaded_count = sum(1 for p in prompts.values() if p is not None)
        logger.info(f"✓ Loaded {loaded_count}/{len(prompts)} prompt templates")
        
        if loaded_count == 0:
            logger.error("No prompts loaded successfully")
            return {}
        
        return prompts
    
    def process_dreams(self) -> None:
        """Process all dreams in the input directory"""
        if not self.processor or not self.writer:
            logger.error("Agent not properly initialized. Cannot process dreams.")
            return
        
        logger.info(f"\nScanning directory: {self.config.input_pdf_dir}")
        
        # Process all files in input directory
        processed_dreams = self.processor.process_directory(self.config.input_pdf_dir)
        
        if not processed_dreams:
            logger.warning("\nNo files were successfully processed.")
            logger.info(f"Please place PDF or TXT files in '{self.config.input_pdf_dir}'")
            return
        
        # Write all outputs
        self.writer.write_batch(processed_dreams)
        
        logger.info(f"\n{'='*60}")
        logger.info("✓ Processing complete!")
        logger.info(f"✓ Check '{self.config.output_dir}' for outputs")
        logger.info(f"{'='*60}")
    
    def process_single_file(self, file_path: Path) -> None:
        """
        Process a single dream file.
        
        Args:
            file_path: Path to the dream file
        """
        if not self.processor or not self.writer:
            logger.error("Agent not properly initialized. Cannot process file.")
            return
        
        processed_dream = self.processor.process_file(file_path)
        
        if processed_dream:
            self.writer.write_processed_dream(processed_dream)
            logger.info("\n✓ File processed successfully!")
        else:
            logger.error("\n✗ Failed to process file")