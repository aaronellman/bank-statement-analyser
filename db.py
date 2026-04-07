import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "statements.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                description TEXT,
                amount TEXT,
                balance TEXT,
                accrued_bank_charges TEXT,
                source_file TEXT,
                UNIQUE(date, description, amount, balance, source_file)
            )
        """)


def insert_transactions(transactions: list[dict]):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            """INSERT OR IGNORE INTO transactions
               (date, description, amount, balance, accrued_bank_charges, source_file)
               VALUES (:Date, :Description, :Amount, :Balance, :Accrued_Bank_Charges, :Source_File)""",
            transactions
        )

def select_transactions():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM transactions").fetchall()
