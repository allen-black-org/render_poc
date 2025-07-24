from models import (SessionLocal, DimProducts, FactAUMFlow
, DimTransactionTypes, DimDates, DimWholesalers, DimAccounts, FactRevenue, FactRetentionSnapshots)
from sqlalchemy import func, case
from collections import defaultdict
from flask import Flask, jsonify, send_file, render_template


def get_retention_json():
    session = SessionLocal()
    results = (
        session.query(
            DimWholesalers.wholesaler_name,
            FactRetentionSnapshots.days_since_flow,
            (func.sum(FactRetentionSnapshots.retained_amount) / func.sum(FactAUMFlow.flow_amount)).label(
                "retention"),
        )
        .join(FactRetentionSnapshots.flow)
        .join(FactAUMFlow.wholesaler)
        .group_by(DimWholesalers.wholesaler_name, FactRetentionSnapshots.days_since_flow)
        .order_by(DimWholesalers.wholesaler_name, FactRetentionSnapshots.days_since_flow)
        .all()
    )

    session.close()
    summary = defaultdict(dict)
    for wholesaler, aging, retained in results:
        summary[wholesaler][str(aging)] = round(float(retained), 3)

    return summary