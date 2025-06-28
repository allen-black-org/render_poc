import os
from flask import Flask, jsonify, send_file
from sqlalchemy import func
from models import SessionLocal, Product, AUMFlow, TransactionType

app = Flask(__name__)


@app.route('/')
def home():
    return (
        "Welcome to my Flask BI project!<br><br>"
        "This is a personal, AI-assisted learning app built to explore Python, Flask, and cloud deployment.<br><br>"

        "<strong>Key accomplishments so far:</strong><br>"
        "- Developed a full dimensional data warehouse using PostgreSQL<br>"
        "- Built and deployed a Flask application on Render<br>"
        "- Integrated SQLAlchemy ORM for structured data access and reuse<br>"
        "- Modeled and loaded test data across flows, revenue, expenses, and compensation<br>"
        "- Designed a clean and normalized star schema<br><br>"

        "<strong>Demo & Resources:</strong><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; Demo route: <a href='/flows-summary'>/flows-summary</a> (or visit allenblack.org/flows-summary)<br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; This route demonstrates a live query using SQLAlchemy ORM models<br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; ER Diagram of the Data Warehouse: <a href='/er-diagram'>/er-diagram</a><br><br>"

        "Check back as new features and routes are added over time."
    )

@app.route('/er-diagram')
def er_diagram():
    file_path = os.path.join(os.path.dirname(__file__), 'docs', 'v1.0', 'dist_perf_dw_er_diagram_spaced.png')
    return send_file(file_path, mimetype='image/png')

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
