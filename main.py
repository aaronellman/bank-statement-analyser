from rich import print
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from extractor import get_tables, format_tables

def main():
    console = Console()
    console.rule("[bold]Bank-statement-analyzer")
    
    result = get_tables(input("Path to file: "))

    tables_md, pages = result[0], result[1]
    statements_dict = format_tables(pages)

    print(f"[blue bold]Total Pages: {len(pages)}")
    print(statements_dict)

    response = [print(item.get("Date")) for item in statements_dict]
    rows = len(response)
    print(f"# Of Items: {rows}\nResponse: {response}")
    
    for table in tables_md: 
        md = Markdown(table)
        console.print(md)

if __name__ == "__main__":
    main()
