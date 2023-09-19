import requests
import config

def fetch_weather(city_name):
    try:
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={config.weather_api_key}&units=metric"
        response = requests.get(weather_url)
        data = response.json()

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            weather_message = f"Погода в {city_name}:\n"
            weather_message += f"Стан погоди: {weather_description}\n"
            weather_message += f"Температура: {temperature}°C\n"
            weather_message += f"Вологість: {humidity}%\n"
            weather_message += f"Швидкість вітру: {wind_speed} м/с"

            return weather_message
        else:
            return None
    except Exception as e:
        return None
