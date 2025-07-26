-- stg_dim_transaction_types.sql
{{ config(materialized='view') }}
SELECT id, transaction_type_name, is_inflow, description FROM {{ source('raw', 'dim_transaction_types') }}