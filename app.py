"""Step 1 of the app deploy: Flask backend that reads student names from Postgres and serves a plain HTML page."""
import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)


def get_students():
    with psycopg2.connect(os.environ["DATABASE_URL"]) as conn, conn.cursor() as cur:
        cur.execute("SELECT name, school_year FROM students ORDER BY name")
        return cur.fetchall()


def get_skill_averages():
    """The first 'model': inputs are every row in students, output is four numbers (the averaging happens in SQL)."""
    with psycopg2.connect(os.environ["DATABASE_URL"]) as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT ROUND(AVG(skill_programming), 2),
                   ROUND(AVG(skill_data_stats), 2),
                   ROUND(AVG(skill_frontend_design), 2),
                   ROUND(AVG(skill_business_pitch), 2)
            FROM students""")
        programming, data_stats, frontend_design, business_pitch = cur.fetchone()
    return [("Programming", programming), ("Data and stats", data_stats),
            ("Frontend and design", frontend_design), ("Business and pitch", business_pitch)]


@app.route("/")
def index():
    return render_template("index.html", students=get_students(), averages=get_skill_averages())


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5001)), debug=True)
