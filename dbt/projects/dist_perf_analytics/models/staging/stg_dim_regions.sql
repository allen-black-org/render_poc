-- stg_dim_regions.sql
{{ config(materialized='view') }}
SELECT id, region_name FROM {{ source('raw', 'dim_regions') }}