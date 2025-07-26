-- stg_dim_advisors.sql
{{ config(materialized='view') }}
SELECT id, advisor_name, region_id, channel_id, firm_id, created_at, updated_at FROM {{ source('raw', 'dim_advisors') }}