-- stg_fact_revenue.sql
{{ config(materialized='view') }}
SELECT id, account_id, product_id, wholesaler_id, revenue_date_id, fee_rate, revenue_amount, created_at, updated_at FROM {{ source('raw', 'fact_revenue') }}