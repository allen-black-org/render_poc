-- stg_dim_firm_types.sql
{{ config(materialized='view') }}
SELECT id, firm_type_name FROM {{ source('raw', 'dim_firm_types') }}