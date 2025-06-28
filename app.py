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
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; Demonstration route: <a href='/flows-summary'>/flows-summary</a> (or visit allenblack.org/flows-summary)<br>"
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

@app.route("/flows-summary")
def flows_summary():
    conn = get_db_connection()
    cur = conn.cursor()

    query = """
    SELECT
        p.product_name,
        tt.transaction_type_name,
        SUM(f.flow_amount) AS total_flow
    FROM dist_perf_dw.fact_aum_flows f
    JOIN dist_perf_dw.dim_products p ON f.product_id = p.id
    JOIN dist_perf_dw.dim_transaction_types tt ON f.transaction_type_id = tt.id
    GROUP BY p.product_name, tt.transaction_type_name
    ORDER BY p.product_name, tt.transaction_type_name;
    """

    cur.execute(query)
    results = cur.fetchall()
    cur.close()
    conn.close()

    # Format as nested dict: {product: {inflow: X, outflow: Y, ...}}
    summary = {}
    for product, tx_type, amount in results:
        if product not in summary:
            summary[product] = {}
        summary[product][tx_type] = float(amount)

    return jsonify(summary)

if __name__ == '__main__':
    app.run()
