import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StoryBookGenerator:
    """
    Generates a PDF storybook from the collected stories.
    """
    
    def __init__(self, template: str = "classic"):
        self.template = template

    def create_book(self, title: str, author: str, chapters: List[Dict]) -> str:
        """
        Compiles stories into a PDF format.
        Args:
            chapters: List of {"title": "...", "content": "..."}
        Returns:
            Path to generated PDF.
        """
        logger.info(f"Generating book '{title}' by {author} with {len(chapters)} chapters.")
        
        # logic using FPDF or ReportLab would go here
        # For prototype, we generate a markdown/text representation
        
        output_content = f"# {title}\nBy {author}\n\n"
        for chap in chapters:
            output_content += f"## {chap['title']}\n\n{chap['content']}\n\n"
            
        return "/tmp/generated_book_mock.pdf"
        
    def add_photo(self, photo_path: str, caption: str):
        pass
