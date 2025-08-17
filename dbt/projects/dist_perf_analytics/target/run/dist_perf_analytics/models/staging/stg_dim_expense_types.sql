
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_expense_types
  
  
  
  
  as (
    -- stg_dim_expense_types.sql

SELECT id, expense_type_name, expense_type_category_id, is_fixed, created_at, updated_at FROM dist_perf_db.dist_perf_staging.dim_expense_types
  );

