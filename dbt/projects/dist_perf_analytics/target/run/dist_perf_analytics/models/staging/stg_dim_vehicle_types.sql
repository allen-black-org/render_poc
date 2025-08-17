
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_vehicle_types
  
  
  
  
  as (
    -- stg_dim_vehicle_types.sql

SELECT id, vehicle_type_name FROM dist_perf_db.dist_perf_staging.dim_vehicle_types
  );

