-- stg_dim_territories.sql
{{ config(materialized='view') }}
SELECT id, territory_name, territory_code, region_id, country_name, created_at, updated_at FROM {{ source('raw', 'dim_territories') }}