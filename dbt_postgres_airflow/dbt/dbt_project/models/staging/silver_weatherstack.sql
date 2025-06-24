{{ config(
    materialized='table',
    unique_key='id'
    )
}}

WITH source AS (
    SELECT * FROM {{ source("dev", "bronze_weatherstack_raw")}}
),

de_duplicate AS (
    SELECT *,
        row_number() OVER (PARTITION BY time order by inserted_at) as row_number
    FROM source
)

SELECT id,
        city,
        temperature,
        weather_description,
        wind_speed,
        time as weather_time_local,
        (inserted_at + (utc_offset || 'hours')::interval) as inserted_time_local
        
FROM de_duplicate
WHERE row_number = 1