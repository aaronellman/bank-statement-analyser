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
                amount REAL,
                category TEXT,
                balance REAL,
                accrued_bank_charges REAL,
                UNIQUE(date, description, amount, balance)
            )""")

        #storing custom categories created by user
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE,
                category TEXT
            )""")
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS imported_files (
            file_hash TEXT PRIMARY KEY,
            source_file TEXT,
            imported_at datetime DEFAULT CURRENT_TIMESTAMP)
            """)


def insert_transactions(transactions: list[dict]):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            """INSERT OR IGNORE INTO transactions
                      (date, description, amount, category, balance, accrued_bank_charges)
               VALUES (:Date, :Description, :Amount, :Category, :Balance, :Accrued_Bank_Charges)""",
            transactions
        )


def select_transactions():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT * FROM transactions").fetchall()


def select_transaction_trunc_date():
    """returns sqlite3 rows that have the date truncated to Y-M for trend analysis"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        result = conn.execute("""
                              SELECT strftime('%Y-%m', date) AS cleaned_date, category, SUM(amount) as amount 
                              FROM transactions
                              WHERE amount < 0 
                              GROUP BY cleaned_date, category
                              ORDER BY cleaned_date ASC""").fetchall()

        return result


def select_categories():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(row) for row in conn.execute("SELECT * FROM categories").fetchall()]


def select_categories_display():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT keyword, category FROM categories").fetchall()


def category_exists(keyword: str):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute(
            "SELECT 1 FROM categories where keyword = ?", (keyword,)
        ).fetchone()

        return result


def insert_categories(rules: list[dict]):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            """INSERT OR IGNORE INTO categories
               (keyword, category)
               VALUES (:Keyword, :Category)""",
            rules
        )


def delete_category(keyword: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "DELETE FROM categories where keyword = ?", (keyword,)
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

def insert_imported_files(imported: list[tuple]):
    with sqlite3.connect(DB_PATH) as conn:
        conn.executemany(
            """INSERT OR IGNORE INTO imported_files
               (file_hash, source_file)
               VALUES (?,?)""",
               imported  
        )

def select_hashed_file(file_hash: str):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute("""
                        SELECT file_hash from imported_files
                        WHERE file_hash = ?
                        """, (file_hash,)).fetchone()
        
        return result
