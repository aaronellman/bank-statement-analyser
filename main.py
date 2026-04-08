from rich import print
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from extractor import get_tables, format_tables
from db import init_db, insert_transactions, select_transactions, select_summary
import typer

app = typer.Typer()
console = Console()
console.rule("[bold]Bank-statement-analyzer")
init_db()

def _show_sql_results(func, *args, **kwargs): #*args and **kwargs
    t = Table(*args)
    for row in func(**kwargs):
        t.add_row(*[str(v) for v in row])
    console.print(t)


@app.command("import")
def import_statement(path: str):
    
    result = get_tables(path)
    tables_md, pages = result[0], result[1]
    statements_dict = format_tables(pages)
    
    insert_transactions(statements_dict)
    _show_sql_results(select_transactions, "ID", "Date", "Description", "Amount", "Category", "Balance", "Accrued")
    

@app.command("summary")
def summary(month: str = None):
    _show_sql_results(select_summary, "Category", "Total Spend", month=month)
    

if __name__ == "__main__":
    app()
