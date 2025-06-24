{{ config(
    materialized='table',
    unique_key='id'
    )
}}

select * FROM {{ source("dev", "bronze_weatherstack_raw")}}

