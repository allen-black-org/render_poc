
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_firms
  
  
  
  
  as (
    -- stg_dim_firms.sql

SELECT id, firm_name, firm_type_id, headquarters_city, headquarters_country, created_at, updated_at FROM dist_perf_db.dist_perf_staging.dim_firms
  );

