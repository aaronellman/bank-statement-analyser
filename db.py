import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "statements.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount TEXT,
                category TEXT,
                balance TEXT,
                accrued_bank_charges TEXT,
                source_file TEXT,
                UNIQUE(date, description, amount, balance, source_file)
            )""")
            
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE,
                category TEXT
            )""")


def insert_transactions(transactions: list[dict]):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            """INSERT OR IGNORE INTO transactions
                      (date, description, amount, category, balance, accrued_bank_charges, source_file)
               VALUES (:Date, :Description, :Amount, :Category, :Balance, :Accrued_Bank_Charges, :Source_File)""",
            transactions
        )


def select_transactions():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM transactions").fetchall()


def select_rules():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute("SELECT * FROM rules").fetchall()]
    

def insert_rules(rules: list[dict]):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            """INSERT OR IGNORE INTO rules
               (keyword, category)
               VALUES (:Keyword, :Category)""",
            rules
        )


def delete_rule(keyword: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM rules where keyword == ?", (keyword,)
        )


def select_summary(month=None): # month, meaning month in a given year format: YYYY-MM
    base_sql = "SELECT category, SUM(amount) from transactions"
    
    with sqlite3.connect(DB_PATH) as conn:
        if not month:
            result = conn.execute(base_sql + "GROUP BY category").fetchall()
        else:
            result = conn.execute(base_sql + " WHERE date LIKE ? GROUP BY category", (month + "%",)).fetchall()

        return result
