import pymupdf
from pathlib import Path
import re
from datetime import datetime
from categorise import categorise
from db import select_hashed_file
import hashlib

def get_tables(path: str):
    """returns markdown of the tables in the statement and the tables themselves"""

    p = Path(path)
    files = list(p.iterdir()) if p.is_dir() else [p]

    markdowns = []
    pages = []
    for file in files:
        doc = pymupdf.open(file)
        
        file_bytes = file.read_bytes()
        file_hash = _get_hash(file_bytes)

        result = select_hashed_file(file_hash)

        if result:
            continue
        
        start_date,end_date = _extract_statement_period(doc)
        for page in doc:
            
            for table in page.find_tables():
                markdowns.append(table.to_markdown())
            pages.append((page, str(file), start_date, end_date, file_hash))

    return markdowns, pages


def _find_header_idx(table_data: list) -> int | None:
    for i, row in enumerate(table_data):
        if row and "Date" in row and "Amount" in row:
            return i
    return None


def _parse_amount(row: list, amount_idx: int) -> str:
    amount = row[amount_idx]
    if row[amount_idx + 1] == 'Cr':
        amount += "Cr"
    return amount


def _sign_amount(amount: str):
    if "Cr" in amount:
        return amount.replace("Cr", "").replace(',', '').strip()
    return f"-{amount}".replace(',', '')


def _table_to_dicts(table_data: list, path: str, start_date, end_date, file_hash) -> list[dict]:
    header_idx = _find_header_idx(table_data)
    if header_idx is None:
        return []

    headers = table_data[header_idx]
    amount_idx = headers.index("Amount")

    return [
        {
            'Date': _resolve_year(row[headers.index('Date')], start_date, end_date),
            'Description': (desc := row[headers.index('Description')]),
            'Amount': _sign_amount(_parse_amount(row, amount_idx)),
            'Category': categorise(desc, None),
            'Balance': row[headers.index('Balance')],
            'Accrued_Bank_Charges': row[headers.index('Accrued\nBank\nCharges')],
            'Source_File': path,
            "File_Hash": file_hash
        }
        for row in table_data[header_idx + 1:]
    ]


def _extract_statement_period(doc):
    text = doc[0].get_text()
    
    m = re.search(r"Statement Period\s*:\s*(\d{1,2}\s+\w+\s+\d{4})\s+to\s+(\d{1,2}\s+\w+\s+\d{4})", text)
    start,end = m.group(1), m.group(2)
    start_date,end_date = datetime.strptime(start, "%d %B %Y"), datetime.strptime(end, "%d %B %Y")
    
    return start_date,end_date


def _resolve_year(date_str: str, start_date: datetime, end_date: datetime) -> str:
    parsed = datetime.strptime(date_str.strip(), "%d %b")
    
    for year in {start_date.year, end_date.year}:
        candidate = parsed.replace(year=year).date()
        
        if start_date.date() <= candidate <= end_date.date():
            return candidate.isoformat()
    
    raise ValueError(f"Could not resolve year for '{date_str}' within {start_date} to {end_date}")

def _get_hash(file_content: bytes):
    return hashlib.sha256(file_content).hexdigest()


def format_tables(pages) -> list[dict]:
    """takes the pages that get_tables returns and returning a list of dictionaries for insertion into db"""

    return [
        entry
        for page, path, start_date, end_date, file_hash in pages
        for table in page.find_tables()
        for entry in _table_to_dicts(table.extract(),path, start_date, end_date, file_hash)
    ]
