# bank-statement-analyzer

A Python CLI tool that parses PDF bank statements, stores transactions in a local SQLite database, and surfaces spending insights.

## Features

- **PDF parsing** - extracts transactions from one or more PDF bank statements using `pymupdf`
- **Local storage** - persists transactions in a SQLite database with deduplication so re-importing the same file is safe
- **Auto-categorisation** - maps transaction descriptions to categories via keyword rules (e.g. `UBER` → `Transport`)
- **Spending insights** - summarises spending by category or month
- **Rich terminal UI** - tables and colours via `rich`

## Transaction shape

Each transaction is stored with the following fields:

| Field | Type | Description |
|---|---|---|
| `date` | `str` | ISO 8601 date, e.g. `2024-01-15` |
| `description` | `str` | Raw merchant/payee string from the statement |
| `amount` | `float` | Negative = debit, positive = credit |
| `category` | `str` | Auto-assigned category or `uncategorised` |
| `balance` | `float` | Running account balance after the transaction |
| `accrued_bank_charges` | `float` | Accrued bank charges at time of transaction |

## Installation

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/your-username/bank-statement-analyzer.git
cd bank-statement-analyzer
uv sync
```

## Usage

### Import statements

Parse one or more PDF files and load their transactions into the database:

```bash
uv run python main.py import january_2024.pdf
uv run python main.py import statements/*.pdf
```

Re-importing the same file will not create duplicate records.

### View a spending summary

Display a breakdown of spending by category:

```bash
uv run python main.py summary
```

Filter by month:

```bash
uv run python main.py summary --month 2024-01
```

## Categorisation

Transactions are categorised by matching keywords (case-insensitive) against the transaction description. A set of built-in defaults covers common merchants automatically.

Transactions that match no keyword are stored as `uncategorised`.

## Project structure

```
bank-statement-analyzer/
├── main.py          # CLI entry point and commands
├── extractor.py     # PDF parsing and transaction extraction
├── db.py            # SQLite database access and queries
├── categorise.py    # Keyword-to-category matching logic
├── pyproject.toml   # Project metadata and dependencies
├── uv.lock          # Locked dependency versions
└── statements.db    # SQLite database (created on first import)
```

## Dependencies

| Package | Purpose |
|---|---|
| `pymupdf` | Extract text and tables from PDF files |
| `typer` | CLI argument parsing and command routing |
| `rich` | Terminal formatting, tables, and progress display |

## Development

```bash
# Install dependencies
uv sync

# Run the CLI
uv run python main.py --help
```
