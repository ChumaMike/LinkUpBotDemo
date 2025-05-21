import requests

API_KEY = "18de3bc153e610217b281073e9767a8c"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]['temp']
        desc = data["weather"][0]["description"].capitalize()
        humidity = data['main']['humidity']
        
        return f"Weather in {city.title()}:\n Temparature: {temp}°C\n Description: {desc}\n Humidity: {humidity}%"
    else:
        return "Could not find that city. Please check the name and try again."