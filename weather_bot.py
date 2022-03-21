import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

# button_weather = KeyboardButton('Узнать погоду \U00002600')
# greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_weather)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет! Напиши название города и узнай погоду!')


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': '\U00002600 Ясно',
        'Clouds': '\U00002601 Облачно',
        'Rain': '\U00002614 Дождь',
        'Drizzle': '\U00002614 Дождь',
        'Thunderstorm': '\U000026A1 Гроза',
        'Snow': '\U0001F328 Снег',
        'Mist': '\U0001F32B Туман'
    }
    
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=ru"
        )
        data = r.json()
        
        city = data['name']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
       
        wether_description = data['weather'][0]['main']
        
        if wether_description in code_to_smile:
            wd = code_to_smile[wether_description]
        else:
            wd = '\U0001F525'
        
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).time()
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).time()
        day_length = datetime.datetime.fromtimestamp(data['sys']['sunset'] - data['sys']['sunrise']).time()
        
        await message.reply(f"*{datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}*\n"
              f"*Погода в городе {city}*\n\n{wd}\n"
              f"\U0001F321 Температура *{temp}°С*\n"
              f"\U0001F4A7 Влажность *{humidity}%*\n"
              f"\U0001F300 Давление *{int(pressure * 0.75)} мм.рт.ст*\n"
              f"\U0001F32C Ветер *{wind_speed} м/с*\n\n"
              f"\U0001F305 Восход солнца *{sunrise}*\n"
              f"\U0001F307 Закат солнца *{sunset}*\n"
              f"\U0001F3D9 Продолжительность дня *{day_length}*\n\n"
              f"*\U0001F31F Хорошего дня, {message.from_user.first_name}!*", parse_mode='Markdown'
              )
         
    except:
        await message.reply('\U00002620 Проверьте название города')


if __name__ == '__main__':
    executor.start_polling(dp)