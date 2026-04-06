from rich import print
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from extractor import get_tables, format_tables

def main():
    console = Console()
    console.rule("[bold]Bank-statement-analyzer")
    
    result = get_tables(input("Path to file: "))

    tables_md, tables = result[0], result[1]
    
    formatted_result = format_tables(tables)

    print(f"[blue bold]Total Pages: {len(tables)}")

    print(formatted_result)
    
    for table in tables_md: 
        md = Markdown(table)
        console.print(md)

if __name__ == "__main__":
    main()
