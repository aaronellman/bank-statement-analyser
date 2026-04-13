from rich import print
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from extractor import get_tables, format_tables
from db import (init_db, insert_transactions, select_transactions,
                select_summary, select_uncategorised, insert_imported_files)
import typer
from pathlib import Path

app = typer.Typer()
console = Console()
console.rule("[bold]Bank-statement-analyzer")

def _show_sql_results(func, *args, **kwargs): #*args and **kwargs
    t = Table(*args)
    for row in func(**kwargs):
        t.add_row(*[str(v) for v in row])
    console.print(t)


@app.command("import")
def import_statement(path: str, replace_db: bool = False):

    if replace_db:
        dir_path = Path().cwd()
        db_path = Path(f"{dir_path}/statements.db")
        db_path.unlink(missing_ok=True)
        print(f"[red bold underline] Removed: {db_path}")

    init_db()
    
    result = get_tables(path)
    tables_md, pages, imported = result[0], result[1], result[2]
    statements_dict = format_tables(pages)
    
    insert_transactions(statements_dict)
    
    insert_imported_files(imported)

    _show_sql_results(select_transactions, "ID", "Date", "Description", "Amount", "Category", "Balance", "Accrued")
    

@app.command("summary")
def summary(month: str = None):
    init_db()
    _show_sql_results(select_summary, "Category", "Earnings", "Spendings", month=month)


@app.command("show-uncategorised")
def show_uncategorised(month: str = None):
    init_db()
    _show_sql_results(select_uncategorised, "Date", "Description", "Amount", month=month)
    

if __name__ == "__main__":
    app()
