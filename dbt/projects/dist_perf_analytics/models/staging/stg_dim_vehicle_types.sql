-- stg_dim_vehicle_types.sql
{{ config(materialized='view') }}
SELECT id, vehicle_type_name FROM {{ source('raw', 'dim_vehicle_types') }}