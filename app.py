import os
from flask import Flask, jsonify, send_file
from sqlalchemy import func
from models import SessionLocal, DimProducts, FactAUMFlow, DimTransactionTypes, DimDates
from collections import defaultdict

app = Flask(__name__)


@app.route('/')
def home():
    # 🔹 Home route: static info about the app and links to demo routes & ER diagram
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
    # 🔹 ER Diagram route: returns a PNG file from docs directory
    file_path = os.path.join(os.path.dirname(__file__), 'docs', 'v1.0', 'dist_perf_dw_er_diagram_spaced.png')
    return send_file(file_path, mimetype='image/png')

@app.route("/flows-summary")
def flows_summary():
    # 🔹 Flows summary route: aggregates FactAUMFlow data by year, product, and transaction type
    session = SessionLocal()

    results = (
        session.query(
            DimDates.year_number,
            DimProducts.product_name,
            DimTransactionTypes.transaction_type_name,
            func.sum(FactAUMFlow.flow_amount)
        )
        .join(FactAUMFlow.product)
        .join(FactAUMFlow.transaction_type)
        .join(FactAUMFlow.year)
        .group_by(DimDates.year_number, DimProducts.product_name, DimTransactionTypes.transaction_type_name)
        .order_by(DimDates.year_number, DimProducts.product_name, DimTransactionTypes.transaction_type_name)
        .all()
    )

    session.close()

    # 🔹 Convert query results into nested dict: year → product → tx_type → amount
    summary = defaultdict(lambda: defaultdict(dict))
    for year, product, tx_type, amount in results:
        summary[year][product][tx_type] = float(amount)
    return jsonify(summary)

# 🔹 Legacy example: manual dict-building method (commented out)
""" Old dictionary method without using defaultdic. This explicitly defines layers
    summary = {}
    for year, product, tx_type, total in results:
        year = str(year)

        if year not in summary:
            summary[year] = {}
        if product not in summary[year]:
            summary[year][product] = {}
        summary[year][product][tx_type] = float(total)

    return jsonify(summary)
"""

if __name__ == '__main__':
    # 🔹 Local dev server runner
    app.run()
