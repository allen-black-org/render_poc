-- stg_dim_wholesalers.sql
{{ config(materialized='view') }}
SELECT id, wholesaler_name, team_lead_id, hire_date, territory_id, created_at, updated_at FROM {{ source('raw', 'dim_wholesalers') }}