import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

# utility functions that jerry can call when in 'coder' mode
# should also add a proper regular function calling mode but 'coder' mode works pretty damn well

# TODO: make a real send_message function that sends a message to a phone number or contact
def send_message(message):
    print(message)

api_key = os.getenv('WEATHER_API_KEY')
# # TODO: get the lat and lon from the web interface
lat = float(os.getenv('LAT'))
lon = float(os.getenv('LON'))
print(lat, lon)

def get_weather():
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'metric'}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        print(weather_data)
        return weather_data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

todos = []
with open('./todolist.json', 'r') as f:
    todos = json.load(f)

def add_todo(todo):
    todos.append(todo)
    with open('./todolist.json', 'w') as f:
        json.dump(todos, f)
    return todos

def remove_todo(index):
    del todos[index]
    with open('./todolist.json', 'w') as f:
        json.dump(todos, f)
    return todos


def get_todos():
    # print(todos)
    return todos



