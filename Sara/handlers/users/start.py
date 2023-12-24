import sqlite3
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.main_keyboards import keyboards
from loader import dp, db, bot
from utils.misc import subscription
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(
        text=f"<b>Assalomu alaykum {message.from_user.get_mention()}, botimizga xush kelibsiz</b>\n\n"
             f"🎥 Bot orqali siz sevimli filmlar, seriallar va multfilmlarni sifatli formatda ko'rishingiz mumkin\n\n"
             f"<b>Quyidagi menudan kerakli bo'limni tanlang👇</b>",reply_markup=keyboards
    )
