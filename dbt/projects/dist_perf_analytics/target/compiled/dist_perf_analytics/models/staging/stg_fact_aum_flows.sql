-- stg_fact_aum_flows.sql

SELECT id, date_id, account_id, wholesaler_id, advisor_id, product_id, channel_id, transaction_type_id, flow_amount, account_aum_amount, created_at, updated_at FROM dist_perf_db.dist_perf_staging.fact_aum_flows