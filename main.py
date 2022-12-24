from aiogram import Bot, Dispatcher, types, executor
import requests
from dataclasses import dataclass

from bs4 import BeautifulSoup as BS

import pytz
from geopy import GoogleV3

# погода
from pyowm import OWM
from pyowm.utils.config import get_default_config


bot = Bot('5848782264:AAEXbLQ6lsSAApMR4Z4lQ3m5lpHFmqsSVjc')
dp = Dispatcher(bot)
now_city = ''


def is_valid(url):
    check = requests.get(url)
    if check.status_code == 200:
        return True
    elif check.status_code == 404:
        return False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    mess = f'Привет, <b>{message.from_user.first_name} {message.from_user.last_name}</b>, ' \
           f'введи назавание города о котором ты хочешь получить информацию о погоде.'
    await bot.send_message(message.chat.id, mess, parse_mode='html')


@dp.message_handler()
async def check_city(msg: types.Message):
    global now_city
    now_city = msg.text
    url = f'https://ru.wikipedia.org/wiki/{now_city}'
    if (is_valid(url)):

        config_dict = get_default_config()
        config_dict['language'] = 'ru'

        owm = OWM('2e8a65f8f73b20ed812a0fc06669838f', config_dict)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(now_city)
        global weath
        weath = observation.weather


        markup = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        website = types.KeyboardButton(text='Wiki-страница', callback_data='website')
        weather = types.KeyboardButton(text='погода', callback_data='all_info')
        location = types.KeyboardButton(text='температура', callback_data='temperature')
        time = types.KeyboardButton(text='скорость ветра', callback_data='wind_speed')
        cartoon = types.KeyboardButton(text='влажность', callback_data='humidity')

        markup.add(weather, website, location, time, cartoon)
        await msg.answer('Информация о данном городе', reply_markup=markup)
    else:
        await msg.answer('Неверно введено название города, попробуйте еще раз')


@dp.callback_query_handler(lambda callback: callback.data)
async def answer_website(callback):
    if callback.data == 'website':
        url = f'https://ru.wikipedia.org/wiki/{now_city}'
        await bot.send_message(callback.message.chat.id, url)

    elif callback.data == 'all_info':
        config_dict = get_default_config()
        config_dict['language'] = 'ru'

        t = weath.temperature("celsius")
        t1 = t['temp']
        t2 = t['feels_like']
        t3 = t['temp_max']
        t4 = t['temp_min']

        wi = weath.wind()['speed']
        humi = weath.humidity
        cl = weath.clouds
        st = weath.status
        dt = weath.detailed_status
        ti = weath.reference_time('iso')
        pr = weath.pressure['press']
        vd = weath.visibility_distance

        await bot.send_message(callback.message.chat.id, "В городе " + str(now_city) + " температура " + str(t1) + " °C" + "\n" +
                         "Максимальная температура " + str(t3) + " °C" + "\n" +
                         "Минимальная температура " + str(t4) + " °C" + "\n" +
                         "Ощущается как " + str(t2) + " °C" + "\n" +
                         "Скорость ветра " + str(wi) + " м/с" + "\n" +
                         "Давление " + str(pr) + " мм.рт.ст" + "\n" +
                         "Влажность " + str(humi) + " %" + "\n" +
                         "Видимость " + str(vd) + "  метров" + "\n" +
                         "Описание " + str(dt))

    elif callback.data == 'temperature':
        config_dict = get_default_config()
        config_dict['language'] = 'ru'

        temp = weath.temperature("celsius")['temp']
        if temp > 16:
            await bot.send_sticker(callback.message.chat.id, sticker='CAACAgIAAxkBAAEG-RZjpe4wch3nLkhuDl22QphGQMLsIAACbQMAAmOLRgzx0bSyjf2I7SwE')
        else:
            await bot.send_sticker(callback.message.chat.id, sticker='CAACAgIAAxkBAAEG-Rhjpe5RNgPk0tm0fI8mtVajDJrrEAACbgMAAmOLRgyw9Y-wNTkiGywE')

        await bot.send_message(callback.message.chat.id, f"Температура в городе {now_city} сейчас состовляет {temp}",
                               parse_mode='html')

    elif callback.data == 'wind_speed':
        config_dict = get_default_config()
        config_dict['language'] = 'ru'

        temp = weath.wind()['speed']
        if temp > 10:
            await bot.send_photo(callback.message.chat.id, 'https://kipmu.ru/wp-content/uploads/veter-1.jpg')
        if temp < 5:
            await bot.send_photo(callback.message.chat.id, 'https://elims.org.ua/pritchi/files/2012/11/pritcha-veter-i-cvetok.jpg')
        else:
            await bot.send_photo(callback.message.chat.id, 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Kizhi_06-2017_img23_windsock.jpg/1920px-Kizhi_06-2017_img23_windsock.jpg')
        await bot.send_message(callback.message.chat.id, f"Скорость ветра в городе {now_city} сейчас состовляет {temp}",
                               parse_mode='html')

    elif callback.data == 'humidity':
        config_dict = get_default_config()
        config_dict['language'] = 'ru'

        temp = weath.humidity
        if temp > 50:
            await bot.send_video(callback.message.chat.id, 'https://media.istockphoto.com/id/1055362144/ru/%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE/%D0%B2%D0%B5%D1%82%D0%BA%D0%B0-%D0%B4%D0%B5%D1%80%D0%B5%D0%B2%D0%B0-%D1%81-%D1%86%D0%B2%D0%B5%D1%82%D0%B0%D0%BC%D0%B8-%D0%B2-%D0%B4%D0%BE%D0%B6%D0%B4%D1%8C-%D1%81%D1%8A%D0%B5%D0%BC%D0%BA%D0%B8-%D1%81-%D0%BA%D0%B0%D0%BC%D0%B5%D1%80%D0%BE%D0%B9-%D0%B7%D0%B0%D0%BC%D0%B5%D0%B4%D0%BB%D0%B5%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE-%D0%B4%D0%B2%D0%B8%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F.mp4?s=mp4-640x640-is&k=20&c=q7JviKcIdL8ftU3HyhiEizX3Ab1dCpEItfIMX5spzr0=')
        else:
            await bot.send_video(callback.message.chat.id, 'https://media.istockphoto.com/id/1251361061/ru/%D0%B2%D0%B8%D0%B4%D0%B5%D0%BE/%D0%B7%D0%B0%D0%BA%D0%B0%D1%82-time-lapse-%D0%BD%D0%B0%D0%B4-%D0%B2%D0%B5%D0%BB%D0%B8%D1%87%D0%B5%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%BC-%D0%BF%D1%83%D1%81%D1%82%D1%8B%D0%BD%D0%BD%D1%8B%D0%BC-%D0%BB%D0%B0%D0%BD%D0%B4%D1%88%D0%B0%D1%84%D1%82%D0%BE%D0%BC-%D0%BD%D0%B0%D0%BC%D0%B8%D0%B1%D0%B8%D1%8F-%D0%B0%D1%84%D1%80%D0%B8%D0%BA%D0%B0.mp4?s=mp4-640x640-is&k=20&c=LzEHcYV7EmV637mqZfrSdOBjy_2OD-WUPYW-zr04C7M=')

        await bot.send_message(callback.message.chat.id, f"Влажность в городе {now_city} сейчас состовляет {temp}", parse_mode='html')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
