-- stg_fact_aum_flows.sql
{{ config(materialized='view') }}
SELECT id, date_id, account_id, wholesaler_id, advisor_id, product_id, channel_id, transaction_type_id, flow_amount, account_aum_amount, created_at, updated_at FROM {{ source('raw', 'fact_aum_flows') }}
