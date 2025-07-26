-- stg_dim_expense_types.sql
{{ config(materialized='view') }}
SELECT id, expense_type_name, expense_type_category_id, is_fixed, created_at, updated_at FROM {{ source('raw', 'dim_expense_types') }}