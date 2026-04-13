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
                file_hash TEXT,
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
                      (date, description, amount, category, balance, accrued_bank_charges, source_file, file_hash)
               VALUES (:Date, :Description, :Amount, :Category, :Balance, :Accrued_Bank_Charges, :Source_File, :File_Hash)""",
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
    params = []

    sql = """SELECT category, 
            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income, 
            SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) as spending 
            FROM transactions
            """
    
    if month:
        sql +=  "WHERE date LIKE ? GROUP BY category"
        params.append((month + "%"))
    else:
        sql += "GROUP BY category"

    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute(sql, params).fetchall()
        return result
    

def select_uncategorised(month=None):
    with sqlite3.connect(DB_PATH) as conn:
        if not month:
            result = conn.execute("""
                            SELECT date, description, amount
                            FROM transactions 
                            WHERE category = 'uncategorised'
                             """).fetchall()
        else:
            result = conn.execute("""
                                SELECT date, description, amount
                                FROM transactions 
                                WHERE category = 'uncategorised' AND date LIKE ?
                                """, (month + "%",)).fetchall()
        
        return result
    

def select_hashed_file(file_hash: str):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("""
                        SELECT file_hash from transactions
                        WHERE file_hash = ?
                        """, (file_hash,)).fetchone()
        
        return result
