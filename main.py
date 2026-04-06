from rich import print
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from extractor import get_tables

def main():
    console = Console()
    console.rule("[bold]Bank-statement-analyzer")
    tables = get_tables(input("Path to file: "))

    print(f"[blue bold]Total Pages: {len(tables)}")
    
    for table in tables: 
        md = Markdown(table)
        console.print(md)

if __name__ == "__main__":
    main()
