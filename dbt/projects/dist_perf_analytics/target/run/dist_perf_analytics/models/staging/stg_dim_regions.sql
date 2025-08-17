
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_regions
  
  
  
  
  as (
    -- stg_dim_regions.sql

SELECT id, region_name FROM dist_perf_db.dist_perf_staging.dim_regions
  );

