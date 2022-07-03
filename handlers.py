from main import bot, dp
from aiogram import types
from config import ADMIN_ID, WEATHER_TOKEN
import requests
import datetime

async def send_to_admin(dp):
    await bot.send_message(chat_id=ADMIN_ID, text='bot started')

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='В каком городе ты хочешь узнать погоду?')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text='Напиши название города')


@dp.message_handler()
async def message_weather(message: types.Message):
    def get_city_coord(city, weather_token):
        try:
            data = requests.get(
                f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={weather_token}').json()
            return (data[0]['lat'], data[0]['lon'])
        except:
            pass

    def get_weather(lat, lon, weather_token):
        try:
            data = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_token}&units=metric&lang=ru').json()
            return f'В основном: {data["weather"][0]["description"]}\nТемпература: {data["main"]["temp"]} C°\nОщущается как: {data["main"]["feels_like"]} C°' \
                   f'\nВлажность: {data["main"]["humidity"]}%\nДавление: {data["main"]["pressure"]} мм.рт.ст\nСкорость ветра: {data["wind"]["speed"]}м/с' \
                   f'\nВосход солнца: {datetime.datetime.fromtimestamp(data["sys"]["sunrise"])}\nЗакат солнца: {datetime.datetime.fromtimestamp(data["sys"]["sunset"])}'
        except:
            pass


    city = message.text
    lat,lon = get_city_coord(city,WEATHER_TOKEN)
    await message.answer(text=get_weather(lat,lon,WEATHER_TOKEN))



