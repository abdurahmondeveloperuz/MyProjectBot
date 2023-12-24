import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from loader import channels
from utils.misc import subscription
from loader import db, banuser,bot
import datetime
import sqlite3

class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self,update:types.Update,data:dict):
        if update.message:
            user = update.message.from_user.id
            fullname_for = update.message.from_user.first_name
            username_for = update.message.from_user.username
            text = "message"
        elif update.callback_query:
            user = update.callback_query.from_user.id
            fullname_for = update.callback_query.from_user.first_name
            username_for = update.callback_query.from_user.username
            text = update.callback_query.data
            await update.callback_query.answer(cache_time=5)
            if text =="check_subs":
                await update.callback_query.message.delete()
        else:
            return
            
        if banuser.check_user(user):
            btn = InlineKeyboardMarkup(row_width=1)
            btn.add(InlineKeyboardButton(text=f"👮‍♂️Admindan uzur so'rash",url=f"https://t.me/clone_account"))
            if text == "message":
                await update.message.answer("<b>❌Siz botda bloklangansiz!</b>\n\n\n<i>👇🏻Pastdagi tugmani bosish orqali admindan uzur so'rashingiz va blokdan olinishingiz mumkin!</i>",reply_markup=btn)
            else:

                await update.callback_query.message.answer("<b>❌Siz botda bloklangansiz!</b>\n\n\n<i>👇🏻Pastdagi tugmani bosish orqali admindan uzur so'rashingiz va blokdan chiqishingiz mumkin!</i>",reply_markup=btn)
            raise CancelHandler()
        try:

            user_get = await bot.get_chat(user)   
            user_bio = user_get.bio
            db.add_user(id=user,fullname=fullname_for,username=username_for)
            count = db.count_users()[0]
            await bot.send_message(chat_id='-1002123033592',text=f"""\n🆕 Yangi foydalanuvchi!\n🆔 Foydalanuvchi idsi:  <code>{user}</code>\n📛 Foydalanuvchi: {update.message.from_user.get_mention()}\n🌐 Foydalanuvchi useri:  {username_for}\n📍 Foydalanuvchi biosi:  {user_bio} \n➖➖➖➖➖➖➖➖➖➖➖\n🖐Umumiy: {count}""")
        except:pass
        buttons = InlineKeyboardMarkup(row_width=1)
        final_status = True 
        CHANNELS = channels.get_channels()
        for channel in CHANNELS:
            status = await subscription.check(user_id=user, channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if not status:
                invite_link = await channel.export_invite_link()
                buttons.add(InlineKeyboardButton(text=f"{channel.title}",url=f"{invite_link}"))
        if not final_status:
            buttons.add(InlineKeyboardButton(text="✅Obuna bo'ldim",callback_data="check_subs"))
            if update.message:await update.message.answer('⚠️ Botdan foydalanish uchun, quyidagi kanallarga obuna bo\'ling:',reply_markup=buttons)
            else:await update.callback_query.message.answer('⚠️ Botdan foydalanish uchun, quyidagi kanallarga obuna bo\'ling:',reply_markup=buttons)
            raise CancelHandler()

        

