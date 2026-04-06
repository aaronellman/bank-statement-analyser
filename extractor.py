import pymupdf
from pathlib import Path

def get_tables(path: str):
    p = Path(path)
    files = list(p.iterdir()) if p.is_dir() else [p]

    tables = []
    for file in files:
        doc = pymupdf.open(file)

        for page in doc:
            tables += page.find_tables()

    return [table.to_markdown() for table in tables]

