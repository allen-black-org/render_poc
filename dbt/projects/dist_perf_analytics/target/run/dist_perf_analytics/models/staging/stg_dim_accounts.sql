
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_accounts
  
  
  
  
  as (
    -- stg_dim_accounts.sql

SELECT id, account_name, account_code, base_fee_rate, created_at, updated_at FROM dist_perf_db.dist_perf_staging.dim_accounts
  );

