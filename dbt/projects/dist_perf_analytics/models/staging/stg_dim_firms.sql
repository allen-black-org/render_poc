-- stg_dim_firms.sql
{{ config(materialized='view') }}
SELECT id, firm_name, firm_type_id, headquarters_city, headquarters_country, created_at, updated_at FROM {{ source('raw', 'dim_firms') }}