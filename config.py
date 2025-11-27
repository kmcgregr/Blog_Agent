# config.py
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field

class Config(BaseModel):
    """Configuration settings for the Dream Agent"""
    
    # LLM Settings
    llm_model: str = Field(default="gpt-oss:20b", description="Ollama model name")
    llm_temperature: float = Field(default=0.7, description="LLM temperature")
    llm_base_url: Optional[str] = Field(default="http://localhost:11434", description="Ollama base URL")
    
    # Directory Settings
    input_pdf_dir: Path = Field(default=Path("input_dreams/"), description="Input directory")
    output_dir: Path = Field(default=Path("processed_dreams/"), description="Output directory")
    chroma_db_path: Path = Field(default=Path("chroma_db/"), description="ChromaDB path")
    
    # Prompt File Paths
    prompts_dir: Path = Field(default=Path("prompts/"), description="Prompts directory")
    correction_prompt_file: str = Field(default="correction_prompt.xml")
    title_prompt_file: str = Field(default="title_prompt.xml")
    story_prompt_file: str = Field(default="story_prompt.xml")
    copy_edit_prompt_file: str = Field(default="copy_edit_prompt.xml")
    story_review_prompt_file: str = Field(default="story_review_prompt.xml")
    image_prompt_file: str = Field(default="image_prompt_gen_prompt.xml")
    
    # Processing Settings
    max_retries: int = Field(default=3, description="Max retries for LLM calls")
    timeout: int = Field(default=300, description="Timeout for LLM calls in seconds")
    
    class Config:
        arbitrary_types_allowed = True
    
    def get_prompt_path(self, prompt_file: str) -> Path:
        """Get full path for a prompt file"""
        return self.prompts_dir / prompt_file
    
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist"""
        self.input_pdf_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_db_path.mkdir(parents=True, exist_ok=True)
        self.prompts_dir.mkdir(parents=True, exist_ok=True)

# Global config instance
config = Config()