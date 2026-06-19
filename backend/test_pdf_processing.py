from rag.pdf_parser import extract_text
from rag.chunker import create_chunks
from pathlib import Path

pdf_path = Path(__file__).parent.parent / "data" / "AWS Customer Agreement.pdf"

text = extract_text(str(pdf_path))

chunks = create_chunks(text)

print(len(chunks))