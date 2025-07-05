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
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; Demo routes: These routes demonstrate live queries using SQLAlchemy ORM models<br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/revenue-product-monthly-summary'>/revenue-product-monthly-summary</a><br>"
       " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/revenue-efficiency-summary'>/revenue-efficiency-summary</a><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/revenue-wholesaler-summary'>/revenue-wholesaler-summary</a><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/account-flows-summary'>/account-flows-summary</a><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; ER Diagram of the Data Warehouse: <a href='/er-diagram'>/er-diagram</a><br><br>"

        "Check back as new features and routes are added over time."
    )
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route('/er-diagram')
def er_diagram():
    # 🔹 ER Diagram route: returns a PNG file from docs directory
    file_path = os.path.join(os.path.dirname(__file__), 'docs', 'v1.0', 'Distribution_Performance_ERD.png')
    return send_file(file_path, mimetype='image/png')
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/account-flows-summary")
def account_flows_summary():
    # 🔹 Flows summary route: aggregates FactAUMFlow data by year, product, and transaction type
    session = SessionLocal()

    results = (
        session.query(
            DimAccounts.account_name,
            DimDates.year_number,
            DimTransactionTypes.transaction_type_name,
            func.sum(FactAUMFlow.flow_amount)
        )
        .join(FactAUMFlow.account)
        .join(FactAUMFlow.transaction_type)
        .join(FactAUMFlow.year)
        .group_by(DimDates.year_number, DimAccounts.account_name, DimTransactionTypes.transaction_type_name)
        .order_by(DimAccounts.account_name, DimDates.year_number, DimTransactionTypes.transaction_type_name)
        .limit(100)
        .all()
    )

    session.close()

    return jsonify([
        {"account": account, "year": year, "tx_type": tx_type, "flow_amount": float(flow_amount)}
        for account, year, tx_type, flow_amount in results])

    # 🔹 Convert query results into nested dict: year → product → tx_type → amount
    """summary = defaultdict(lambda: defaultdict(dict))
    for account, year, tx_type, amount in results:
        summary[account][year][tx_type] = float(amount)
    return jsonify(summary)"""
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/revenue-efficiency-summary")
def revenue_efficiency_summary():
    # 🔹 AUM summary route: aggregates aum data by wholesaler
    session = SessionLocal()

    results = (
        session.query(
            DimWholesalers.wholesaler_name,
            func.sum(FactAUMFlow.account_aum_amount).label("total-aum"),
            func.sum(FactAUMFlow.account_aum_amount*DimAccounts.base_fee_rate).label("total-revenue"),
            (func.sum(FactAUMFlow.account_aum_amount * DimAccounts.base_fee_rate)/func.sum(FactAUMFlow.account_aum_amount)).label("effective_fee_rate")
        )
        .join(FactAUMFlow.wholesaler)
        .join(FactAUMFlow.account)
        .group_by(DimWholesalers.wholesaler_name)
        .order_by(DimWholesalers.wholesaler_name)
        .all()
    )

    session.close()
    return jsonify([
        {"wholesaler": wholesaler, "aum": float(total_aum), "revenue": float(total_revenue), "efr": float(efr)}
        for wholesaler, total_aum, total_revenue, efr in results])
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/revenue-product-monthly-summary")
def revenue_product_monthly_summary():

    session = SessionLocal()

    results = (
        session.query(
            DimProducts.product_name,
            DimDates.full_date,
            func.sum(FactRevenue.revenue_amount),
        )
        .join(FactRevenue.product)
        .join(FactRevenue.revenue_date)
        .group_by(DimProducts.product_name, DimDates.full_date)
        .order_by(DimProducts.product_name, DimDates.full_date)
        .limit(100)
        .all()
    )
    session.close()

    return jsonify([
        {"product": product, "month": month, "revenue": float(revenue)}
        for product, month, revenue in results])

    # 🔹 Convert query results into nested dict: product → month → revenue
    """summary = defaultdict(lambda: defaultdict(dict))
    for product, month, revenue in results:
        summary[product][month.isoformat()] = float(revenue)
    return jsonify(summary)"""
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/revenue-wholesaler-summary")
def revenue_wholesaler_summary():

    session = SessionLocal()

    results = (
        session.query(
            DimWholesalers.wholesaler_name,
            func.sum(FactRevenue.revenue_amount),
        )
        .join(FactRevenue.rev_wholesaler)
        .group_by(DimWholesalers.wholesaler_name)
        .order_by(DimWholesalers.wholesaler_name)
        .limit(100)
        .all()
    )
    session.close()
    return jsonify([
        {"wholesaler": wholesaler, "revenue": revenue}
        for wholesaler, revenue in results])
"""-----------------------------------------------------------------------------------------------------------------"""


if __name__ == '__main__':
    # 🔹 Local dev server runner
    app.run()
