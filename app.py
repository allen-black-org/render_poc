import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return (
        "Welcome to my Flask BI project!<br><br>"
        "This is a personal, AI-assisted learning app built to explore Python, Flask, and cloud deployment.<br><br>"
        "The goals of this project include:<br>"
        "- Building interactive web applications using Flask<br>"
        "- Connecting to and querying a PostgreSQL database<br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; Demonstration route: <a href='/dbtest'>/dbtest</a> (or visit allenblack.org/dbtest)<br>"
        "- Transforming and presenting data using Python<br>"
        "- Deploying apps to the cloud via Render<br><br>"
        "Check back as new features and routes are added over time."
    )
#db connection for local docker postgres
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d1djjc3ipnbc73dbvi6g-a.virginia-postgres.render.com",
        database="pocdb_te73",
        user="pocdb_te73_user",
        password="TnlIBboc9mOqMrXWiYd1hiseRWpiCbPN"
    )
    return conn

#route for local docker postgres
@app.route("/dbtest")
def test_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM dist_perf_dw.dim_expense_types limit 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    formatted = [f"{r[0]} {r[1]}  {r[2]} {r[3]}" for r in rows]
    return "<br>".join(formatted)

# Additional route that returns structured JSON
@app.route('/pocdb')
def poc_db():
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute('SELECT NOW()')
        result = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify({"db_time": str(result[0])})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run()
