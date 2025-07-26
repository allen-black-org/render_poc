-- stg_fact_distribution_expense.sql
{{ config(materialized='view') }}
SELECT id, wholesaler_id, date_id, expense_type_id, is_adjustment, expense_notes, expense_amount, created_at, updated_at FROM {{ source('raw', 'fact_distribution_expense') }}
