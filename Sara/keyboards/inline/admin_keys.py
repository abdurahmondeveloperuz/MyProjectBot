from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import bot
AdminPanel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📣 Reklama yuborish", callback_data='admin:send_ad'),
            InlineKeyboardButton(text="🗄 Bazani yuklash", callback_data='admin:base'),

        ],
        [

            InlineKeyboardButton(text="❌ Foydalanuvchilarni o'chirish", callback_data='admin:delete_users'),
            InlineKeyboardButton(text="🚫 Blok qilish", callback_data='admin:block'),

        ],
        [
            InlineKeyboardButton(text="🎬 Kino qo'shish",callback_data="add_kino")
        ],
        [
            InlineKeyboardButton(text="📢 Kanal sozlamari",callback_data="admin:channels")

        ],
        [
            InlineKeyboardButton(text="👤 Foydalanuvchiga habar yuborish", callback_data='admin:send_user'),
        ],
    ],
)

GoToAdminPanel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀ Admin Panelga qaytish", callback_data='GoToAdminPanel')
        ]
    ]
)

SendAd_Type = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📋 Oddiy habar", callback_data='oddiy_habar'),
            InlineKeyboardButton(text="↪ Forward habar", callback_data='forward_habar')
        ],
        [
            InlineKeyboardButton(text="◀ Admin Panelga qaytish", callback_data='GoToAdminPanel')
        ]
    ],
)


backDelete = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🚫 Bekor qilish", callback_data='GoToAdminPanel')
        ]
    ]
)

DeleteUsers = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data='delete:verify'),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data='GoToAdminPanel')
        ]
    ]
)

BaseType = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⚙️ Database", callback_data='database'),
            InlineKeyboardButton(text="📑 Excel", callback_data='excel')
        ],
        [
            InlineKeyboardButton(text="◀️ Ortga", callback_data="GoToAdminPanel")
        ]
    ]
)

answer_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👮‍♂️ Adminga javob berish", callback_data="answer_admin")
        ]
    ]
)

back_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="◀️ Ortga", callback_data='user_back')
        ]
    ]
)




