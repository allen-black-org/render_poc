-- stg_fact_wholesaler_comp.sql
{{ config(materialized='view') }}
SELECT id, wholesaler_id, date_id, base_salary, incentive_comp, notes, created_at, updated_at FROM {{ source('raw', 'fact_wholesaler_comp') }}
