# writers/output_writer.py
from pathlib import Path
from processors.dream_processor import ProcessedDream
import logging

logger = logging.getLogger(__name__)

class OutputWriter:
    """Handles writing processed dream data to files"""
    
    def __init__(self, output_dir: Path):
        """
        Initialize the output writer.
        
        Args:
            output_dir: Directory to write output files
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def write_processed_dream(self, processed_dream: ProcessedDream) -> None:
        """
        Write all processed dream data to separate files.
        
        Args:
            processed_dream: ProcessedDream object containing all data
        """
        base_filename = Path(processed_dream.original_file).stem
        
        # Write corrected dream with title
        self._write_corrected_dream(
            base_filename,
            processed_dream.seo_title,
            processed_dream.corrected_dream_text
        )
        
        # Write story draft
        self._write_story_draft(
            base_filename,
            processed_dream.seo_title,
            processed_dream.short_story_draft
        )
        
        # Write final story
        self._write_final_story(
            base_filename,
            processed_dream.seo_title,
            processed_dream.final_short_story
        )
        
        # Write reviewed story
        self._write_reviewed_story(
            base_filename,
            processed_dream.seo_title,
            processed_dream.reviewed_story
        )
        
        # Write image prompt if available
        if processed_dream.image_prompt:
            self._write_image_prompt(
                base_filename,
                processed_dream.image_prompt
            )
    
    def _write_corrected_dream(self, base_filename: str, title: str, content: str) -> None:
        """Write corrected dream text"""
        output_path = self.output_dir / f"{base_filename}_corrected_dream.md"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(content)
            logger.info(f"✓ Saved corrected dream: {output_path.name}")
        except Exception as e:
            logger.error(f"Error writing corrected dream: {e}")
    
    def _write_story_draft(self, base_filename: str, title: str, content: str) -> None:
        """Write initial story draft"""
        output_path = self.output_dir / f"{base_filename}_story_draft.md"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"## Initial Story Draft for: {title}\n\n")
                f.write(content)
            logger.info(f"✓ Saved story draft: {output_path.name}")
        except Exception as e:
            logger.error(f"Error writing story draft: {e}")
    
    def _write_final_story(self, base_filename: str, title: str, content: str) -> None:
        """Write final copy-edited story"""
        output_path = self.output_dir / f"{base_filename}_final_short_story.md"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"## Final (Copy-Edited) Story for: {title}\n\n")
                f.write(content)
            logger.info(f"✓ Saved final story: {output_path.name}")
        except Exception as e:
            logger.error(f"Error writing final story: {e}")
    
    def _write_reviewed_story(self, base_filename: str, title: str, content: str) -> None:
        """Write reviewed story"""
        output_path = self.output_dir / f"{base_filename}_reviewed_story.md"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"## Reviewed Story for: {title}\n\n")
                f.write(content)
            logger.info(f"✓ Saved reviewed story: {output_path.name}")
        except Exception as e:
            logger.error(f"Error writing reviewed story: {e}")
    
    def _write_image_prompt(self, base_filename: str, content: str) -> None:
        """Write image generation prompt"""
        output_path = self.output_dir / f"{base_filename}_image_prompt.txt"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✓ Saved image prompt: {output_path.name}")
        except Exception as e:
            logger.error(f"Error writing image prompt: {e}")
    
    def write_batch(self, processed_dreams: list[ProcessedDream]) -> None:
        """
        Write multiple processed dreams.
        
        Args:
            processed_dreams: List of ProcessedDream objects
        """
        logger.info(f"\nWriting {len(processed_dreams)} processed dream(s)...")
        for processed_dream in processed_dreams:
            self.write_processed_dream(processed_dream)
            logger.info("-" * 60)