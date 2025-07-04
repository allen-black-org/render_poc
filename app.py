import os
from dotenv import load_dotenv
from flask import Flask, jsonify, send_file
from sqlalchemy import func, case
from models import (SessionLocal, DimProducts, FactAUMFlow
, DimTransactionTypes, DimDates, DimWholesalers, DimAccounts, FactRevenue)
from collections import defaultdict

load_dotenv()
app = Flask(__name__)
"""-----------------------------------------------------------------------------------------------------------------"""
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
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; Demo routes: <br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/revenue-summary'>/revenue-summary</a><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/aum-summary'>/aum-summary</a><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/flows-summary'>/flows-summary</a><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull; This route demonstrates a live query using SQLAlchemy ORM models<br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; ER Diagram of the Data Warehouse: <a href='/er-diagram'>/er-diagram</a><br><br>"

        "Check back as new features and routes are added over time."
    )
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route('/er-diagram')
def er_diagram():
    # 🔹 ER Diagram route: returns a PNG file from docs directory
    file_path = os.path.join(os.path.dirname(__file__), 'docs', 'v1.0', 'dist_perf_dw_er_diagram_spaced.png')
    return send_file(file_path, mimetype='image/png')
"""-----------------------------------------------------------------------------------------------------------------"""
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
        .limit(100)
        .all()
    )

    session.close()

    # 🔹 Convert query results into nested dict: year → product → tx_type → amount
    summary = defaultdict(lambda: defaultdict(dict))
    for year, product, tx_type, amount in results:
        summary[year][product][tx_type] = float(amount)
    return jsonify(summary)
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/aum-summary")
def aum_summary():
    # 🔹 AUM summary route: aggregates aum data by wholesaler
    session = SessionLocal()

    results = (
        session.query(
            DimWholesalers.wholesaler_name,
            (DimAccounts.account_name + '-' + DimAccounts.account_code).label("account_id"),
            DimAccounts.base_fee_rate,
            func.sum(FactAUMFlow.account_aum_amount),
            func.sum(FactAUMFlow.account_aum_amount*DimAccounts.base_fee_rate),
        )
        .join(FactAUMFlow.wholesaler)
        .join(FactAUMFlow.account)
        .filter(FactAUMFlow.account_aum_amount > 0)
        .group_by(DimWholesalers.wholesaler_name, DimAccounts.account_name + '-' + DimAccounts.account_code, DimAccounts.base_fee_rate)
        .order_by(DimWholesalers.wholesaler_name, (DimAccounts.account_name + '-' + DimAccounts.account_code))
        .limit(100)
        .all()
    )

    session.close()
    return jsonify([
        {"wholesaler": name, "account_id": account, "fee_rate": rate, "account_aum": float(aum), "fee_amount": fee}
        for name, account, rate, aum, fee in results])
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/revenue-summary")
def revenue_summary():
    # 🔹 AUM summary route: aggregates aum data by wholesaler
    session = SessionLocal()

    results = (
        session.query(
            DimDates.full_date,
            DimAccounts.account_name,
            DimProducts.product_name,
            DimWholesalers.wholesaler_name,
            FactRevenue.fee_rate,
            func.sum(FactRevenue.revenue_amount),
        )
        .join(FactRevenue.product)
        .join(FactRevenue.rev_account)
        .join(FactRevenue.rev_wholesaler)
        .join(FactRevenue.revenue_date)
        .group_by(DimDates.full_date,
            DimAccounts.account_name,
            DimProducts.product_name,
            DimWholesalers.wholesaler_name,
            FactRevenue.fee_rate)
        .order_by(DimDates.full_date,
            DimAccounts.account_name,
            DimProducts.product_name,
            DimWholesalers.wholesaler_name,
            FactRevenue.fee_rate)
        .limit(100)
        .all()
    )
    session.close()
    return jsonify([
        {"Rev_Date": date, "account": account, "product": product, "wholesaler": wholesaler, "fee_rate": fee_rate, "revenue": revenue}
        for date, account, product, wholesaler, fee_rate, revenue in results])
"""-----------------------------------------------------------------------------------------------------------------"""

if __name__ == '__main__':
    # 🔹 Local dev server runner
    app.run()
