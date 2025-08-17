
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_territories
  
  
  
  
  as (
    -- stg_dim_territories.sql

SELECT id, territory_name, territory_code, region_id, country_name, created_at, updated_at FROM dist_perf_db.dist_perf_staging.dim_territories
  );

