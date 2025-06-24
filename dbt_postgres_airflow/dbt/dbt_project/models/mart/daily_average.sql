{{
    config(
        materialized = 'table'
    )
}}
SELECT city, 
        round(avg(temperature)::numeric, 2) as average_temperature, 
        round(avg(wind_speed)::numeric, 2) as average_windspeed, 
        date(weather_time_local) as date 
FROM {{ref('silver_weatherstack')}}
GROUP BY city, date(weather_time_local)
ORDER BY city, date(weather_time_local)