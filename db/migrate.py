"""Create the schema on Railway Postgres and load data/class_dataset.csv.

Usage (repo root, venv active, DATABASE_URL in .env = Railway's DATABASE_PUBLIC_URL):
    python db/migrate.py          # create tables + load, prints row counts
    python db/migrate.py --reset  # drop the five tables first
"""
import csv, os, sys
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    sys.exit("DATABASE_URL is not set in .env")
if "railway.internal" in DATABASE_URL:
    sys.exit("That is the PRIVATE Railway host. Use DATABASE_PUBLIC_URL locally.")

TABLES = ["student_availability", "student_tools", "availability_slots", "tools", "students"]


def split_multi(cell):
    return [v.strip() for v in (cell or "").split(";") if v.strip() and v.strip() != "none yet"]


def main():
    rows = list(csv.DictReader(open(ROOT / "data" / "class_dataset.csv", newline="", encoding="utf-8")))
    with psycopg2.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        if "--reset" in sys.argv:
            for t in TABLES:
                cur.execute(f"DROP TABLE IF EXISTS {t} CASCADE")
        cur.execute((ROOT / "db" / "schema.sql").read_text())

        for r in rows:
            cur.execute(
                """INSERT INTO students (netid, name, school_year, intro_programming, skill_programming,
                       skill_data_stats, skill_frontend_design, skill_business_pitch,
                       working_style, interests, semester_goal, submitted_at)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (netid) DO UPDATE SET name = EXCLUDED.name
                   RETURNING student_id""",
                (r["netid"].strip().lower(), r["name"].strip(), r["school_year"] or None,
                 r["intro_programming"] or None, r["skill_programming"] or None, r["skill_data_stats"] or None,
                 r["skill_frontend_design"] or None, r["skill_business_pitch"] or None,
                 r["working_style"].strip() or None, r["interests"].strip() or None,
                 r["semester_goal"].strip() or None, r["submitted_at"] or None),
            )
            sid = cur.fetchone()[0]
            for table, col, bridge, fk, cell in [
                ("tools", "name", "student_tools", "tool_id", r["tools"]),
                ("availability_slots", "label", "student_availability", "slot_id", r["availability"]),
            ]:
                for val in split_multi(cell):
                    cur.execute(f"INSERT INTO {table} ({col}) VALUES (%s) ON CONFLICT ({col}) DO UPDATE SET {col} = EXCLUDED.{col} RETURNING {fk}", (val,))
                    cur.execute(f"INSERT INTO {bridge} (student_id, {fk}) VALUES (%s,%s) ON CONFLICT DO NOTHING", (sid, cur.fetchone()[0]))

        for t in reversed(TABLES):
            cur.execute(f"SELECT count(*) FROM {t}")
            print(f"{t:22} {cur.fetchone()[0]}")


if __name__ == "__main__":
    main()
