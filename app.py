import os
from dotenv import load_dotenv
from flask import Flask, jsonify, send_file, render_template, url_for
from sqlalchemy import func, case
from models import (SessionLocal, DimProducts, FactAUMFlow
, DimTransactionTypes, DimDates, DimWholesalers, DimAccounts, FactRevenue, FactRetentionSnapshots)
from collections import defaultdict
from analytics.retention_regression import compute_retention_slopes
from analytics.retention_data import get_retention_json

load_dotenv()
app = Flask(__name__)
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route('/')
def home():
    try:
        with open("last_deploy.txt", "r") as f:
            deploy_time = f.read().strip()
    except FileNotFoundError:
        deploy_time = "Unknown"
    return render_template('home_split.html', deploy_time=deploy_time)

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
    return jsonify(get_retention_json())
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/retention-outliers")
def retention_outliers():
    retention_data = get_retention_json()
    modeled = compute_retention_slopes(retention_data)
    return modeled
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/retention-chart")
def retention_chart():
    return render_template("retention_chart.html")

if __name__ == '__main__':
    # 🔹 Local dev server runner
    app.run()
