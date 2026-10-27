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


@app.route("/")
def index():
    return render_template("index.html", students=get_students())


if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5001)), debug=True)
