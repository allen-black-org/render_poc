import os
from models_sf import (DimProductsSF, FactAUMFlowSF
, DimTransactionTypesSF, DimDatesSF, DimWholesalersSF, DimAccountsSF, FactRevenueSF, FactRetentionSnapshotsSF)
from sqlalchemy import func, case
from collections import defaultdict
from flask import Flask, jsonify, send_file, render_template
from connections import SessionPG, SessionSF

def get_retention_json():
    session = SessionSF()
    results = (
        session.query(
            DimWholesalersSF.wholesaler_name,
            FactRetentionSnapshotsSF.days_since_flow,
            (func.sum(FactRetentionSnapshotsSF.retained_amount) / func.sum(FactAUMFlowSF.flow_amount)).label(
                "retention"),
        )
        .join(FactRetentionSnapshotsSF.flow)
        .join(FactAUMFlowSF.wholesaler)
        .group_by(DimWholesalersSF.wholesaler_name, FactRetentionSnapshotsSF.days_since_flow)
        .order_by(DimWholesalersSF.wholesaler_name, FactRetentionSnapshotsSF.days_since_flow)
        .all()
    )

    session.close()
    summary = defaultdict(dict)
    for wholesaler, aging, retained in results:
        summary[wholesaler][str(aging)] = round(float(retained), 3)

    return summary