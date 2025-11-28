# processors/dream_processor.py
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from chains.processing_chains import ProcessingChains
from loaders.document_loader import DocumentLoader
import logging

logger = logging.getLogger(__name__)

@dataclass
class ProcessedDream:
    """Container for all processed dream data"""
    original_file: str
    original_text: str
    corrected_dream_text: str
    seo_title: str
    short_story_draft: str
    final_short_story: str
    reviewed_story: str
    image_prompt: Optional[str] = None

class DreamProcessor:
    """Handles the complete dream processing pipeline"""
    
    def __init__(self, processing_chains: ProcessingChains):
        """
        Initialize the dream processor.
        
        Args:
            processing_chains: ProcessingChains instance
        """
        self.chains = processing_chains
        self.document_loader = DocumentLoader()
    
    def process_file(self, file_path: Path) -> Optional[ProcessedDream]:
        """
        Process a single dream file through the entire pipeline.
        
        Args:
            file_path: Path to the dream file
            
        Returns:
            ProcessedDream object or None if processing fails
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {file_path.name}")
        logger.info(f"{'='*60}")
        
        # Load document
        dream_text = self.document_loader.load_document(file_path)
        if dream_text is None:
            logger.error(f"Failed to load document: {file_path}")
            return None
        
        # Step 1: Correct grammar and formatting
        corrected_dream = self.chains.correct_dream(dream_text)
        if corrected_dream is None:
            logger.error("Failed to correct dream text")
            return None
        
        # Step 2: Generate SEO title
        seo_title = self.chains.generate_title(corrected_dream)
        if seo_title is None:
            logger.error("Failed to generate title")
            return None
        
        # Step 3: Generate story draft
        story_draft = self.chains.generate_story(corrected_dream)
        if story_draft is None:
            logger.error("Failed to generate story")
            return None
        
        # Step 4: Copy-edit the story
        final_story = self.chains.copy_edit_story(story_draft)
        if final_story is None:
            logger.error("Failed to copy-edit story")
            return None
        
        # Step 5: Review the story
        reviewed_story = self.chains.review_story(final_story)
        if reviewed_story is None:
            logger.error("Failed to review story")
            return None
        
        # Step 6: Generate image prompt (optional)
        image_prompt = self.chains.generate_image_prompt(corrected_dream, story_draft)
        
        # Create ProcessedDream object
        processed_dream = ProcessedDream(
            original_file=str(file_path),
            original_text=dream_text,
            corrected_dream_text=corrected_dream,
            seo_title=seo_title,
            short_story_draft=story_draft,
            final_short_story=final_story,
            reviewed_story=reviewed_story,
            image_prompt=image_prompt
        )
        
        logger.info("✓ Processing complete!")
        return processed_dream
    
    def process_directory(self, input_dir: Path) -> list[ProcessedDream]:
        """
        Process all dream files in a directory.
        
        Args:
            input_dir: Directory containing dream files
            
        Returns:
            List of ProcessedDream objects
        """
        processed_dreams = []
        
        # Get all PDF and TXT files
        files = list(input_dir.glob("*.pdf")) + list(input_dir.glob("*.txt"))
        
        if not files:
            logger.warning(f"No PDF or TXT files found in {input_dir}")
            return processed_dreams
        
        logger.info(f"Found {len(files)} file(s) to process")
        
        for file_path in files:
            processed_dream = self.process_file(file_path)
            if processed_dream:
                processed_dreams.append(processed_dream)
        
        return processed_dreams