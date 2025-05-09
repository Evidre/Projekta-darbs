from flask import Flask, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


def get_db_connection():
    """
    Izveido un atgriež savienojumu ar SQLite datubāzi.
    """
    db = Path(__file__).parent / "aircraft_info.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/aircrafts")
def aircrafts():
    conn = get_db_connection()
    aircrafts = conn.execute("SELECT * FROM aircrafts").fetchall()
    conn.close()
    return render_template("aircrafts.html", aircrafts=aircrafts)


@app.route("/aircrafts/<int:aircraft_id>")
def aircrafts_show(aircraft_id):
    conn = get_db_connection()
    aircraft = conn.execute(
        "SELECT * FROM aircrafts WHERE id = ?",
        (aircraft_id,),
    ).fetchone()
    conn.close()
    return render_template("aircrafts_show.html", aircraft=aircraft)


if __name__ == "__main__":
    app.run(debug=True)
