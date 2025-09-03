# seed_word_difficulties.py
import os
import pandas as pd
from unicodedata import normalize

from app import create_app             # your factory
from database.init_db import db, WordDifficulty

CSV_PATH = os.getenv("CSV_PATH", "datasets/data_with_predictions.csv")

def canonicalize(w: str) -> str:
    # Match your cleaning in the app: NFKC + strip
    return normalize("NFKC", (w or "")).strip()

def to_bool(x):
    # CSV likely has 0/1; cast robustly to bool
    try:
        return bool(int(x))
    except Exception:
        return bool(x)

def main():
    app = create_app()
    with app.app_context():
        print(f"Loading CSV: {CSV_PATH}")
        df = pd.read_csv(CSV_PATH)

        # Rename to match your model exactly
        # CSV columns seen: word,count,log_count,length,syllables,is_homophone,pronunciation_count,user_difficulty_score
        df = df.rename(columns={"user_difficulty_score": "difficulty_score"})

        # Canonicalize + drop empty/dupes
        df["word"] = df["word"].astype(str).map(canonicalize)
        df = df[df["word"] != ""].drop_duplicates(subset=["word"])

        # Cast types
        df["count"] = df["count"].astype(int)
        df["log_count"] = df["log_count"].astype(float)
        df["length"] = df["length"].astype(int)
        df["syllables"] = df["syllables"].astype(float)
        df["is_homophone"] = df["is_homophone"].map(to_bool)
        df["pronunciation_count"] = df["pronunciation_count"].astype(int)
        df["difficulty_score"] = df["difficulty_score"].astype(float)

        # Fetch existing words to avoid IntegrityError on unique
        existing = {
            w for (w,) in db.session.query(WordDifficulty.word).all()
        }
        to_insert = df[~df["word"].isin(existing)]

        print(f"Existing rows: {len(existing)}  |  New rows to insert: {len(to_insert)}")

        # Bulk insert in chunks to keep memory/transaction sizes sane
        BATCH = 5000
        rows = to_insert.to_dict(orient="records")
        for i in range(0, len(rows), BATCH):
            chunk = rows[i:i+BATCH]
            db.session.bulk_insert_mappings(WordDifficulty, chunk)
            db.session.commit()
            print(f"Inserted {i+len(chunk)}/{len(rows)}")

        total = db.session.query(WordDifficulty).count()
        print(f"Done. word_difficulties rows: {total}")

if __name__ == "__main__":
    main()
