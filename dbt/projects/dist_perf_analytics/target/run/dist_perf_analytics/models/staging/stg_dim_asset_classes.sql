
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_asset_classes
  
  
  
  
  as (
    -- stg_dim_asset_classes.sql

SELECT id, asset_class_name FROM dist_perf_db.dist_perf_staging.dim_asset_classes
  );

