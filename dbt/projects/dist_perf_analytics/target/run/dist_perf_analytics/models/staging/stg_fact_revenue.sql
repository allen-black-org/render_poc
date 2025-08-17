
  create or replace   view dist_perf_db.dist_perf_staging.stg_fact_revenue
  
  
  
  
  as (
    -- stg_fact_revenue.sql

SELECT id, account_id, product_id, wholesaler_id, revenue_date_id, fee_rate, revenue_amount, created_at, updated_at FROM dist_perf_db.dist_perf_staging.fact_revenue
  );

