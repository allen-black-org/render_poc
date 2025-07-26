-- stg_dim_channels.sql
{{ config(materialized='view') }}
SELECT id, channel_name FROM {{ source('raw', 'dim_channels') }}