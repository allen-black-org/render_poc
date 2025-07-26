-- stg_dim_accounts.sql
{{ config(materialized='view') }}
SELECT id, account_name, account_code, base_fee_rate, created_at, updated_at FROM {{ source('raw', 'dim_accounts') }}
