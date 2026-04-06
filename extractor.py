import pymupdf

def get_tables(path: str):
    doc = pymupdf.open(path)
    print(f"Pages: {len(doc)}")


    #tbls = [page.find_tables for page in doc]
    tables = []
    for page in doc:
        tables += page.find_tables()

    return [table.to_markdown() for table in tables]

