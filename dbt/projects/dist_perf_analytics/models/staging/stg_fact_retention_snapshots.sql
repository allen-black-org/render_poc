-- stg_fact_retention_snapshots.sql
{{ config(materialized='view') }}
SELECT flow_id, snapshot_date_id, retained_amount, retention_pct, days_since_flow, created_at, updated_at FROM {{ source('raw', 'fact_retention_snapshots') }}