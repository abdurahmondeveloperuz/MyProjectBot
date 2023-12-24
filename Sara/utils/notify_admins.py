import logging
import pytz 

from aiogram import Dispatcher
from datetime import datetime
from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            start = datetime.now(pytz.timezone('Asia/Tashkent'))
            date = str(start.date())
            time = start.strftime('%H:%M:%S')
            await dp.bot.send_message(admin, f"✅ Bot ishga tushdi\n\n\n<i>📅Sana: {date} |  ⏰Vaqt: {time}</i>")

        except Exception as err:
            print(err)
            pass
