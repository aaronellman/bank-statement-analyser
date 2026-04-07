import pymupdf
from pathlib import Path

def get_tables(path: str):
    """returns markdown of the tables in the statement and the tables themselves"""

    p = Path(path)
    files = list(p.iterdir()) if p.is_dir() else [p]

    markdowns = []
    pages = []
    for file in files:
        doc = pymupdf.open(file)
        for page in doc:
            for table in page.find_tables():
                markdowns.append(table.to_markdown())
            pages.append(page)

    return markdowns, pages


def _find_header_idx(table_data: list) -> int | None:
    for i, row in enumerate(table_data):
        if row and "Date" in row and "Amount" in row:
            return i
    return None


def _parse_amount(row: list, amount_idx: int) -> str:
    amount = row[amount_idx]
    if row[amount_idx + 1] == 'Cr':
        amount += 'Cr'
    return amount


def _table_to_dicts(table_data: list) -> list[dict]:
    header_idx = _find_header_idx(table_data)
    if header_idx is None:
        return []

    headers = table_data[header_idx]
    amount_idx = headers.index("Amount")

    return [
        {
            'Date': row[headers.index('Date')],
            'Description': row[headers.index('Description')],
            'Amount': _parse_amount(row, amount_idx),
            'Balance': row[headers.index('Balance')],
            'Accrued Bank Charges': row[headers.index('Accrued\nBank\nCharges')],
        }
        for row in table_data[header_idx + 1:]
    ]


def format_tables(pages) -> list[dict]:
    """takes the pages that get_tables returns and returning a list of dictionaries for insertion into db"""
    return [
        entry
        for page in pages
        for table in page.find_tables()
        for entry in _table_to_dicts(table.extract())
    ]