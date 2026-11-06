from datetime import datetime
import requests

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url, timeout=10)
    return response.text

def get_user_city():
    return "Muzaffarpur"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name" : "get_current_time",
            "description": "Returns the current date and time as a formatted string.",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name" : "get_city_weather",
            "description" : "This tool returns the current or live weather of a given city.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "city" : {
                        "type" : "string",
                        "description" : "city to get the weather for.",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name" : "get_user_city",
            "description" : "Returns the city where the user lives. Use this when the user says 'my city', 'where I live', or 'my location'",
            "parameters" : {
                "type" : "object",
                "properties" : {},
            },
        },
    },
]

FN_NAME_TO_FN_MAP = {
    "get_current_time" : get_current_time,
    "get_city_weather" : get_city_weather,
    "get_user_city" : get_user_city,
}