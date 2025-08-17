
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_firm_types
  
  
  
  
  as (
    -- stg_dim_firm_types.sql

SELECT id, firm_type_name FROM dist_perf_db.dist_perf_staging.dim_firm_types
  );

