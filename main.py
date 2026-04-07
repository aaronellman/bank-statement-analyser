from rich import print
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from extractor import get_tables, format_tables
from db import init_db, insert_transactions, select_transactions

def main():
    console = Console()
    console.rule("[bold]Bank-statement-analyzer")
    
    result = get_tables(input("Path to file: "))
    
    tables_md, pages = result[0], result[1]
    
    statements_dict = format_tables(pages)

    init_db()
    insert_transactions(statements_dict)

    print(f"[blue bold]Total Pages: {len(pages)}")
    print(statements_dict)

    response = [print(item.get("Date")) for item in statements_dict]
    rows = len(response)
    #print(f"# Of Items: {rows}\nResponse: {response}")

    t = Table("ID", "Date", "Description", "Amount", "Balance", "Accrued", "Source File")
    for row in select_transactions():
        t.add_row(*[str(v) for v in row])
    console.print(t)
    
    """for table in tables_md: 
        md = Markdown(table)
        console.print(md)"""

if __name__ == "__main__":
    main()
