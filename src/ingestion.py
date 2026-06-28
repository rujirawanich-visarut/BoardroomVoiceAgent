import os
from src.contracts import DocumentContext

class DocumentIngestionAgent:
    def __init__(self):
        pass

    def ingest(self, file_path: str) -> DocumentContext:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Could not find input file: {file_path}")
            
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            
        # Split by double newlines for paragraphs
        paragraphs = [p.strip() for p in raw_text.split('\n\n') if p.strip()]
        
        return DocumentContext(
            raw_text=raw_text,
            paragraphs=paragraphs
        )
