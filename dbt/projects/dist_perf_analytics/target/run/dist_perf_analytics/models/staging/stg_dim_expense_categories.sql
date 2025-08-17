
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_expense_categories
  
  
  
  
  as (
    -- stg_dim_expense_categories.sql

SELECT id, category_name FROM dist_perf_db.dist_perf_staging.dim_expense_categories
  );

