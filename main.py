#!/usr/bin/env python3
# main.py
"""
Dream Journal Processing Agent
Processes dream journal entries into blog-ready content using LangChain and Ollama.
"""

import argparse
import logging
import sys
from pathlib import Path

from config import config, Config
from agents.dream_agent import DreamAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('dream_agent.log')
    ]
)

logger = logging.getLogger(__name__)

def setup_argparse() -> argparse.ArgumentParser:
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Process dream journal entries into blog content using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all files in input directory
  python main.py
  
  # Use a different model
  python main.py --model mistral
  
  # Process a single file
  python main.py --file input_dreams/my_dream.pdf
  
  # Use custom directories
  python main.py --input dreams/ --output blog_posts/
        """
    )
    
    parser.add_argument(
        '--model',
        default=config.llm_model,
        help=f'Ollama model to use (default: {config.llm_model})'
    )
    
    parser.add_argument(
        '--input',
        type=Path,
        default=config.input_pdf_dir,
        help=f'Input directory for dream files (default: {config.input_pdf_dir})'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=config.output_dir,
        help=f'Output directory for processed files (default: {config.output_dir})'
    )
    
    parser.add_argument(
        '--file',
        type=Path,
        help='Process a single file instead of the entire directory'
    )
    
    parser.add_argument(
        '--temperature',
        type=float,
        default=config.llm_temperature,
        help=f'LLM temperature (default: {config.llm_temperature})'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose debug logging'
    )
    
    return parser

def main():
    """Main entry point for the application"""
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Update config with command line arguments
    config.llm_model = args.model
    config.input_pdf_dir = args.input
    config.output_dir = args.output
    config.llm_temperature = args.temperature
    
    # Display welcome message
    print("\n" + "="*60)
    print("Dream Journal Processing Agent")
    print("="*60)
    print(f"Model: {config.llm_model}")
    print(f"Input: {config.input_pdf_dir}")
    print(f"Output: {config.output_dir}")
    print("="*60 + "\n")
    
    try:
        # Initialize the Dream Agent
        agent = DreamAgent(config)
        
        # Process dreams
        if args.file:
            # Process single file
            if not args.file.exists():
                logger.error(f"File not found: {args.file}")
                sys.exit(1)
            logger.info(f"Processing single file: {args.file}")
            agent.process_single_file(args.file)
        else:
            # Process entire directory
            agent.process_dreams()
        
    except KeyboardInterrupt:
        logger.info("\n\nProcessing interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()