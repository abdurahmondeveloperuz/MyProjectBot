from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(
        text="<b><u>📚 Botdan foydalanish qo'llanmasi</u></b>\n\n"
             "1️⃣ @SaraFilmUz kanaliga obuna bo'ling\n\n"
             "2️⃣ Ko'rmoqchi bo'lgan kino kodini nusxalab oling\n\n"
             "3️⃣ Botga kirib «🔍Kino izlash» tugmasini bosing\n\n"
             "4️⃣ Kanaldan nusxalab olingan kino kodini kiriting\n\n"
             "5️⃣ Kod mavjud bolsa bot sizga kinoni tashlab beradi\n"
             "➖➖➖➖➖➖➖\n"
             "<b>📣 Botga yoki kanalga reklama bermoqchimisiz?</b>\n\n"
             "🔗 @OnlyAdsUz kanaliga kirib reklama tariflari bilan tanishib chiqin. "
             "Undan so'ng esa <a href='tg://user?id=6011359652'>adminga</a> murojaat qiling"
    )
