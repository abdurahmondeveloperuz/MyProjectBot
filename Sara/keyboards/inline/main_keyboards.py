from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import bot
about_film_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        
        
        [
            InlineKeyboardButton(text="🌐 Davlat", callback_data='country'),
            InlineKeyboardButton(text="📁 Hajm", callback_data="size")
        ],
        [
            InlineKeyboardButton(text="💿 Sifat", callback_data='quality'),
            InlineKeyboardButton(text="⏰ Davomiylik", callback_data='continuity'),
            
        ],
        [
            InlineKeyboardButton(text="🚩 Til", callback_data="language"),
            InlineKeyboardButton(text="🎭 Janr", callback_data='genre')

            ],
        [
            InlineKeyboardButton(text="✅ Bo'ldi", callback_data='past'),
        ],
        [
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data='GoToAdminPanel')

        ]
])
keyboards = InlineKeyboardMarkup(inline_keyboard=
	[
		[
			InlineKeyboardMarkup(text = "🔍 Kino qidirish",switch_inline_query_current_chat=""),
			InlineKeyboardMarkup(text = "⭐️ Saqlangan kinolar",switch_inline_query_current_chat="saved_movies"),
	
		],
		[
			InlineKeyboardMarkup(text = "🔄 Guruhga qo'shish",url="https://t.me/SaraFilmUzBot?startgroup=true")

		],
		[
			InlineKeyboardMarkup(text = "🔍 Kod orqali qidirish",callback_data="film___"),
			InlineKeyboardMarkup(text = "🏆 Top 5 kinolar",callback_data="top5")

		],
		[
		],
		[
			InlineKeyboardMarkup(text = "🎲 Random ",callback_data="random")
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
accept_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Tasdiqlash", callback_data='accept'),            
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data='GoToAdminPanel'),            
        ],
])