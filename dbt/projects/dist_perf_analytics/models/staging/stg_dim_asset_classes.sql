-- stg_dim_asset_classes.sql
{{ config(materialized='view') }}
SELECT id, asset_class_name FROM {{ source('raw', 'dim_asset_classes') }}