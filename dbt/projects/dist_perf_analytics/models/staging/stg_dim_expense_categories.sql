-- stg_dim_expense_categories.sql
{{ config(materialized='view') }}
SELECT id, category_name FROM {{ source('raw', 'dim_expense_categories') }}