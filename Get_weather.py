import requests

weather_api = "246a19779efed202XXXc9e35fe137bd"


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_info = {
            "city": data["name"],
            "weather": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
        return weather_info
    else:
        return None
