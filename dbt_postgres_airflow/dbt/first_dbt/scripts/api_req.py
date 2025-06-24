import requests
from pprint import pprint

base_url = "http://api.weatherstack.com/current"
api_key = "d1963a071c7dd60c53c598395df4112a"  # Note: This appears to be a real API key - you should keep this private!


def fetch_weather_data(api_key, location):
    """
    Fetches current weather data from Weatherstack API
    
    Args:
        api_key (str): Your Weatherstack API access key
        location (str): City name or coordinates (e.g., "New York" or "40.7128,-74.0060")
    
    Returns:
        dict: JSON response containing weather data
        None: If the request fails
    """
    params = {
        'access_key': api_key,
        'query': location
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# weather_data = fetch_weather_data(api_key, "New York")
# if weather_data:
#     pprint(weather_data)

def mock_data_fetch():
    return {'current': {'air_quality': {'co': '379.25',
                             'gb-defra-index': '2',
                             'no2': '27.38',
                             'o3': '75',
                             'pm10': '25.53',
                             'pm2_5': '24.79',
                             'so2': '8.51',
                             'us-epa-index': '2'},
             'astro': {'moon_illumination': 9,
                       'moon_phase': 'Waning Crescent',
                       'moonrise': '03:12 AM',
                       'moonset': '07:12 PM',
                       'sunrise': '05:26 AM',
                       'sunset': '08:31 PM'},
             'cloudcover': 75,
             'feelslike': 37,
             'humidity': 68,
             'is_day': 'no',
             'observation_time': '06:05 AM',
             'precip': 0,
             'pressure': 1018,
             'temperature': 29,
             'uv_index': 0,
             'visibility': 16,
             'weather_code': 116,
             'weather_descriptions': ['Partly cloudy'],
             'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0004_black_low_cloud.png'],
             'wind_degree': 286,
             'wind_dir': 'WNW',
             'wind_speed': 8},
 'location': {'country': 'United States of America',
              'lat': '40.714',
              'localtime': '2025-06-23 02:05',
              'localtime_epoch': 1750644300,
              'lon': '-74.006',
              'name': 'New York',
              'region': 'New York',
              'timezone_id': 'America/New_York',
              'utc_offset': '-4.0'},
 'request': {'language': 'en',
             'query': 'New York, United States of America',
             'type': 'City',
             'unit': 'm'}}