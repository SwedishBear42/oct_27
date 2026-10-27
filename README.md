# oct_27 — Class 8 deploy redo: class dataset → Railway Postgres

Order of operations (objective first, then the step that serves it):
1. Create GitHub repo → `git clone` it locally (somewhere to store and version the work).
2. Download `class_dataset.csv` from Brightspace → `data/` (the data we want hosted).
3. Have the AI design a schema from the CSV → `db/schema.sql` (students; tools + availability as M:N bridges).
4. Railway → New Project → PostgreSQL (provision an empty Postgres *instance*).
5. `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.
6. Postgres service → Connect → Public Network → Add Public Access (laptop is outside Railway).
7. Variables tab → copy `DATABASE_PUBLIC_URL` → `.env` as `DATABASE_URL=...` (never commit `.env`).
8. `python db/migrate.py` — creates the tables and loads the CSV, prints row counts (verify in Railway's Data tab).
