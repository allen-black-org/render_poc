import os
from dotenv import load_dotenv
from flask import Flask, jsonify, send_file, render_template
from sqlalchemy import func, case
from models import (SessionLocal, DimProducts, FactAUMFlow
, DimTransactionTypes, DimDates, DimWholesalers, DimAccounts, FactRevenue, FactRetentionSnapshots)
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
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/product-efficiency-summary'>/product-efficiency-summary</a><br>"
       " &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/wholesaler-efficiency-summary'>/wholesaler-efficiency-summary</a><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/revenue-wholesaler-summary'>/revenue-wholesaler-summary</a><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/account-flows-summary'>/account-flows-summary</a><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&bull;<a href='/flow-retention-aging'>/flow-retention-aging</a><br>"
        "<br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; ER Diagram of the Data Warehouse: <a href='/er-diagram'>/er-diagram</a><br><br>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; Basic Flow Retention Chart: <a href='/retention-chart'>/retention-chart</a><br><br>"

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
@app.route("/wholesaler-efficiency-summary")
def wholesaler_efficiency_summary():
    # 🔹 AUM summary route: aggregates aum data by wholesaler
    session = SessionLocal()

    results = (
        session.query(
            DimWholesalers.wholesaler_name,
            func.sum(FactAUMFlow.account_aum_amount).label("total-aum"),
            func.sum(FactAUMFlow.account_aum_amount*DimAccounts.base_fee_rate).label("total-revenue"),
            func.count(FactAUMFlow.id).label("count_flows"),
            (func.sum(FactAUMFlow.account_aum_amount * DimAccounts.base_fee_rate)/func.count(FactAUMFlow.id)).label("revenue_per_flow"),
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
        {"wholesaler": wholesaler, "aum": float(total_aum), "revenue": float(total_revenue), "count_flow": count_flows, "revenue_per_flow": revenue_per_flow, "efr": float(efr)}
        for wholesaler, total_aum, total_revenue, count_flows, revenue_per_flow, efr in results])
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/product-efficiency-summary")
def product_efficiency_summary():

    session = SessionLocal()

    results = (
        session.query(
            DimProducts.product_name,
            func.sum(FactAUMFlow.account_aum_amount).label("total-aum"),
            func.sum(FactAUMFlow.account_aum_amount * DimAccounts.base_fee_rate).label("total-revenue"),
            func.count(FactAUMFlow.id).label("count_flows"),
            (func.sum(FactAUMFlow.account_aum_amount * DimAccounts.base_fee_rate) / func.count(FactAUMFlow.id)).label(
                "revenue_per_flow"),
            (func.sum(FactAUMFlow.account_aum_amount * DimAccounts.base_fee_rate) / func.sum(
                FactAUMFlow.account_aum_amount)).label("effective_fee_rate")
        )
        .join(FactAUMFlow.product)
        .join(FactAUMFlow.account)
        .group_by(DimProducts.product_name)
        .order_by(DimProducts.product_name)
        .all()
    )

    session.close()
    return jsonify([
        {"product": product, "aum": float(total_aum), "revenue": float(total_revenue), "count_flow": count_flows,
         "revenue_per_flow": revenue_per_flow, "efr": float(efr)}
        for product, total_aum, total_revenue, count_flows, revenue_per_flow, efr in results])

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
@app.route("/flow-retention-aging")
def flow_retention_aging():

    session = SessionLocal()

    results = (
        session.query(
            DimWholesalers.wholesaler_name,
            FactRetentionSnapshots.days_since_flow,
            func.sum(FactRetentionSnapshots.retained_amount),
        )
        .join(FactRetentionSnapshots.flow)
        .join(FactAUMFlow.wholesaler)
        .group_by(DimWholesalers.wholesaler_name,FactRetentionSnapshots.days_since_flow)
        .order_by(DimWholesalers.wholesaler_name,FactRetentionSnapshots.days_since_flow)
        .all()
    )

    session.close()
    summary = defaultdict(dict)
    for wholesaler, aging, retained in results:
        summary[wholesaler][int(aging)] = float(retained)

    return jsonify(summary)
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/retention-chart")
def retention_chart():
    return render_template("retention_chart.html")

if __name__ == '__main__':
    # 🔹 Local dev server runner
    app.run()
