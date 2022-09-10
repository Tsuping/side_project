import requests


def weather_call(city):
    api_key = '30d4741c779ba94c470ca1f63045390a'

    # user_input = input("Enter city: ")

    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")

    if weather_data.json()['cod'] == '404':
        print("No City Found")
    else:
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])

        return (f"The weather in {city} is: {weather}, The temperature in {city} is: {temp}ºF")
        

