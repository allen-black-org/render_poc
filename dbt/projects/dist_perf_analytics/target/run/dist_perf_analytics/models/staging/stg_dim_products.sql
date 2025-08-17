
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_products
  
  
  
  
  as (
    -- stg_dim_products.sql

SELECT id, product_name, asset_class_id, vehicle_type_id, launch_date, is_active, created_at, updated_at FROM dist_perf_db.dist_perf_staging.dim_products
  );

