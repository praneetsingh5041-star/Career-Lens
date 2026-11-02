import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).parent / "careerlens.db"

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                match_score INTEGER,
                resume_skills TEXT,
                matched_skills TEXT,
                missing_skills TEXT,
                suggestions TEXT
            )
        """)

def save_analysis(label, result):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.execute("""
            INSERT INTO analyses(label,match_score,resume_skills,matched_skills,missing_skills,suggestions)
            VALUES(?,?,?,?,?,?)
        """, (
            label, result["match_score"],
            ", ".join(result["resume_skills"]),
            ", ".join(result["matched_skills"]),
            ", ".join(result["missing_skills"]),
            " | ".join(result["suggestions"])
        ))
        return cur.lastrowid

def get_history():
    with sqlite3.connect(DB_PATH) as con:
        return pd.read_sql_query("""
            SELECT id, label, created_at, match_score, matched_skills, missing_skills
            FROM analyses ORDER BY id DESC
        """, con)

def delete_history(row_id):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("DELETE FROM analyses WHERE id=?", (row_id,))

def export_history_csv():
    return get_history().to_csv(index=False).encode("utf-8")
