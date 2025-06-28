import os
from flask import Flask, jsonify
from sqlalchemy import func
from models import SessionLocal, Product, AUMFlow, TransactionType

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
#def get_db_connection():
#    conn = psycopg2.connect(
#        host="dpg-d1djjc3ipnbc73dbvi6g-a.virginia-postgres.render.com",
#        database="pocdb_te73",
#        user="pocdb_te73_user",
#        password="TnlIBboc9mOqMrXWiYd1hiseRWpiCbPN"
#    )
#    return conn

@app.route("/flows-summary")
def flows_summary():
    session = SessionLocal()

    results = (
        session.query(
            Product.product_name,
            TransactionType.transaction_type_name,
            func.sum(AUMFlow.flow_amount)
        )
        .join(AUMFlow.product)
        .join(AUMFlow.transaction_type)
        .group_by(Product.product_name, TransactionType.transaction_type_name)
        .order_by(Product.product_name, TransactionType.transaction_type_name)
        .all()
    )

    session.close()

    summary = {}
    for product, tx_type, total in results:
        if product not in summary:
            summary[product] = {}
        summary[product][tx_type] = float(total)

    return jsonify(summary)

if __name__ == '__main__':
    app.run()
