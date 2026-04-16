from rich import print
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from extractor import get_tables, format_tables, get_category_total_by_date
from db import (init_db, insert_transactions, select_transactions,
                select_summary, select_uncategorised, insert_imported_files, 
                select_transaction_trunc_date)
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

def _display_trends(func, *args, **kwargs): 
    t = Table(*args)
    rows = list(func(**kwargs))

    for i,row in enumerate(rows):
        is_last_month = (len(rows) -1 == i or row["cleaned_date"] != rows[i + 1]["cleaned_date"])
        
        t.add_row(*[str(round(v, 2) if isinstance(v,float) else str(v)) for v in row], end_section=is_last_month)
    console.print(t)

@app.command("trends")
def get_trends():
    init_db()
    
    rows = select_transaction_trunc_date()
    result = get_category_total_by_date(rows)

    #print(result)
    print("[bold]Showing spendings by category for each Month")
    _display_trends(select_transaction_trunc_date, "Month", "Category", "Total")


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
