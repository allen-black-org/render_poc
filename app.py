import os
from dotenv import load_dotenv
from flask import Flask, jsonify, send_file, render_template, url_for
from sqlalchemy import func, case, text
from models_pg import (DimProductsPG, FactAUMFlowPG, DimWholesalersPG, DimAccountsPG, FactRevenuePG, FactRetentionSnapshotsPG)
from collections import defaultdict
from models_sf import (DimAccountsSF, DimAdvisorsSF, DimProductsSF, FactAUMFlowSF, DimWholesalersSF, FactRevenueSF
                      , DimTransactionTypesSF, DimDatesSF)
from analytics.retention_regression import compute_retention_slopes
from analytics.retention_data import get_retention_json
from analytics.plot_retention_slopes import render_retention_slopes_html
# the two session factoriesDimAdvisorsSF
from connections import SessionPG, SessionSF

load_dotenv()
app = Flask(__name__)

# jinja clean itself
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

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
@app.route("/github-privacy")
def privacy():
    return render_template("privacy_policy.html")
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
    session = SessionSF()

    results = (
        session.query(
            DimAccountsSF.account_name,
            DimDatesSF.year_number,
            DimTransactionTypesSF.transaction_type_name,
            func.sum(FactAUMFlowSF.flow_amount)
        )
        .join(FactAUMFlowSF.account)
        .join(FactAUMFlowSF.transaction_type)
        .join(FactAUMFlowSF.year)
        .group_by(DimDatesSF.year_number, DimAccountsSF.account_name, DimTransactionTypesSF.transaction_type_name)
        .order_by(DimAccountsSF.account_name, DimDatesSF.year_number, DimTransactionTypesSF.transaction_type_name)
        .limit(100)
        .all()
    )

    session.close()

    return jsonify([
        {"account": account, "year": year, "tx_type": tx_type, "flow_amount": float(flow_amount)}
        for account, year, tx_type, flow_amount in results])

"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/wholesaler-efficiency-summary")
def wholesaler_efficiency_summary():
    # 🔹 AUM summary route: aggregates aum data by wholesaler
    session = SessionSF()

    results = (
        session.query(
            DimWholesalersSF.wholesaler_name,
            func.sum(FactAUMFlowSF.account_aum_amount).label("total-aum"),
            func.sum(FactAUMFlowSF.account_aum_amount*DimAccountsSF.base_fee_rate).label("total-revenue"),
            func.count(FactAUMFlowSF.id).label("count_flows"),
            (func.sum(FactAUMFlowSF.account_aum_amount * DimAccountsSF.base_fee_rate)/func.count(FactAUMFlowSF.id)).label("revenue_per_flow"),
            (func.sum(FactAUMFlowSF.account_aum_amount * DimAccountsSF.base_fee_rate)/func.sum(FactAUMFlowSF.account_aum_amount)).label("effective_fee_rate")
        )
        .join(FactAUMFlowSF.wholesaler)
        .join(FactAUMFlowSF.account)
        .group_by(DimWholesalersSF.wholesaler_name)
        .order_by(DimWholesalersSF.wholesaler_name)
        .all()
    )

    session.close()
    return jsonify([
        {"wholesaler": wholesaler, "aum": float(total_aum), "revenue": float(total_revenue), "count_flow": count_flows, "revenue_per_flow": revenue_per_flow, "efr": float(efr)}
        for wholesaler, total_aum, total_revenue, count_flows, revenue_per_flow, efr in results])
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/product-efficiency-summary")
def product_efficiency_summary():

    session = SessionSF()

    results = (
        session.query(
            DimProductsSF.product_name,
            func.sum(FactAUMFlowSF.account_aum_amount).label("total-aum"),
            func.sum(FactAUMFlowSF.account_aum_amount * DimAccountsSF.base_fee_rate).label("total-revenue"),
            func.count(FactAUMFlowSF.id).label("count_flows"),
            (func.sum(FactAUMFlowSF.account_aum_amount * DimAccountsSF.base_fee_rate) / func.count(FactAUMFlowSF.id)).label(
                "revenue_per_flow"),
            (func.sum(FactAUMFlowSF.account_aum_amount * DimAccountsSF.base_fee_rate) / func.sum(
                FactAUMFlowSF.account_aum_amount)).label("effective_fee_rate")
        )
        .join(FactAUMFlowSF.product)
        .join(FactAUMFlowSF.account)
        .group_by(DimProductsSF.product_name)
        .order_by(DimProductsSF.product_name)
        .all()
    )

    session.close()
    return jsonify([
        {"product": product, "aum": float(total_aum), "revenue": float(total_revenue), "count_flow": count_flows,
         "revenue_per_flow": revenue_per_flow, "efr": float(efr)}
        for product, total_aum, total_revenue, count_flows, revenue_per_flow, efr in results])

"""-----------------------------------------------------------------------------------------------------------------"""
@app.route("/revenue-wholesaler-summary")
def revenue_wholesaler_summary():

    session = SessionSF()

    results = (
        session.query(
            DimWholesalersSF.wholesaler_name,
            func.sum(FactRevenueSF.revenue_amount),
        )
        .join(FactRevenueSF.rev_wholesaler)
        .group_by(DimWholesalersSF.wholesaler_name)
        .order_by(DimWholesalersSF.wholesaler_name)
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
"""-----------------------------------------------------------------------------------------------------------------"""
@app.route('/retention-slopes')
def retention_slopes():
    # Delegate chart generation to modular script
    try:
        graph_html = render_retention_slopes_html()
        return render_template('retention_slopes.html', graph_html=graph_html)
    except Exception as e:
        import traceback;
        traceback.print_exc()
        return f"<pre>{traceback.format_exc()}</pre>", 500

if __name__ == '__main__':
    # Forces debug + auto-reload, no env vars needed
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)