-- stg_dim_dates.sql
{{ config(materialized='view') }}
SELECT id, full_date, day_of_week_name, day_of_week_number, week_number, month_number, quarter_number, year_number, is_weekend, is_month_start, is_month_end, is_quarter_start, is_quarter_end, is_year_start, is_year_end, created_at, updated_at FROM {{ source('raw', 'dim_dates') }}
