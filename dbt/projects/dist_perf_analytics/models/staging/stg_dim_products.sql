-- stg_dim_products.sql
{{ config(materialized='view') }}
SELECT id, product_name, asset_class_id, vehicle_type_id, launch_date, is_active, created_at, updated_at FROM {{ source('raw', 'dim_products') }}