-- stg_fact_distribution_expense.sql

SELECT id, wholesaler_id, date_id, expense_type_id, is_adjustment, expense_notes, expense_amount, created_at, updated_at FROM dist_perf_db.dist_perf_staging.fact_distribution_expense