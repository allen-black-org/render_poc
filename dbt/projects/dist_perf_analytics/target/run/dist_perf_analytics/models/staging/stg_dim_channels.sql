
  create or replace   view dist_perf_db.dist_perf_staging.stg_dim_channels
  
  
  
  
  as (
    -- stg_dim_channels.sql

SELECT id, channel_name FROM dist_perf_db.dist_perf_staging.dim_channels
  );

