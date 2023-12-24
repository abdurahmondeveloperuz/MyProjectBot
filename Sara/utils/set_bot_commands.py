from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "🔄 Botni ishga tushurish"),
            types.BotCommand("seach", "🔍 Botda kino qidirish"),
            types.BotCommand("help", "🆘 Bot qo'llanmasi bo'yicha yordam olish"),
            types.BotCommand("top", "🏆 Botda reytingi baland top 5 ta kinoni royhati"),
        ]
    )
