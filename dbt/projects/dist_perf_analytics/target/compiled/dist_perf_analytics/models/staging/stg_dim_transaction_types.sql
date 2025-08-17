-- stg_dim_transaction_types.sql

SELECT id, transaction_type_name, is_inflow, description FROM dist_perf_db.dist_perf_staging.dim_transaction_types