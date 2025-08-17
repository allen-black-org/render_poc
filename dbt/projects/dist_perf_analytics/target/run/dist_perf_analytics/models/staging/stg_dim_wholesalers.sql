
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_wholesalers
  
  
  
  
  as (
    -- stg_dim_wholesalers.sql

SELECT id, wholesaler_name, team_lead_id, hire_date, territory_id, created_at, updated_at FROM dist_perf_db.dist_perf_staging.dim_wholesalers
  );

