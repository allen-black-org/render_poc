-- stg_fact_retention_snapshots.sql

SELECT flow_id, snapshot_date_id, retained_amount, retention_pct, days_since_flow, created_at, updated_at FROM dist_perf_db.dist_perf_staging.fact_retention_snapshots