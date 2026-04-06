import pymupdf
from pathlib import Path

def get_tables(path: str):
    """returns markdown of the tables in the statement and the tables themselves"""

    p = Path(path)
    files = list(p.iterdir()) if p.is_dir() else [p]

    tables = []
    for file in files:
        doc = pymupdf.open(file)

        for page in doc:
            tables += page.find_tables()

    return ([table.to_markdown() for table in tables], tables)


def format_tables(tables):
    """takes the tables that get_tables returns and returning a list of dictionaries for insertion into db"""
    
    for table in tables:
        if "Date" in table.extract()[0] and "Amount" in table.extract()[0]:
            table_data = table.extract()

            headers = table_data[0]
            list_of_dicts = [dict(zip(headers, row)) for row in table_data[1:]]
            print(list_of_dicts)

    return list_of_dicts