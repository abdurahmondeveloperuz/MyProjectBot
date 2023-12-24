from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery, ContentTypes, InputFile
from aiogram.dispatcher import FSMContext
import aiogram
import pytz
from keyboards.inline.main_keyboards import back_user,keyboards
from aiogram import types
from datetime import datetime
from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot, films_db, saved_films, views_db
import datetime as dt
import random
from aiogram.types import InlineQuery, InputTextMessageContent,InputMediaVideo, InlineQueryResultArticle, InlineQueryResult


@dp.inline_handler()
async def handle_inline_query(query: InlineQuery):
    query_text = query.query
    user_id = query.from_user.id
    results = []

    if query_text=="":
        films_list = films_db.get_films_data()
        if len(films_list) < 1:
            article = InlineQueryResultArticle(
        id=1,
        # photo_url="https://i.imgur.com/2HEaBZj.jpg",
        title=f"😔 Hech qanday kino topilmadi ...",
        input_message_content=InputTextMessageContent(f"/start"))
            results.append(article)
        count = 0
        for film in films_list:
            count += 1 
            if count == 29:
                break
            name = film[0]
            quality = film[1]
            code = film[2]
            size = film[3]
            views = views_db.get_views_film(code=code)
            if quality == "0" or quality == None:
                title = f"{name}"
            else:
                title = f"{name}, {quality}p"
            article = InlineQueryResultArticle(
        id=code,
        # photo_url="https://i.imgur.com/2HEaBZj.jpg",
        thumb_url="https://i.imgur.com/RxbHv6V.jpg",
        title=title,
        description=f"📁 Hajmi: {size}\n👁Ko'rishlar: {views}",
        input_message_content=InputTextMessageContent(f"/search {code}"))
            results.append(article)
    elif query_text == "saved_movies":
        films_list = saved_films.get_saved_movies(user=user_id)
        if len(films_list) < 1:
            article = InlineQueryResultArticle(
        id=1,
        # photo_url="https://i.imgur.com/2HEaBZj.jpg",
        title=f"😔 Hech qanday kino topilmadi ...",
        input_message_content=InputTextMessageContent(f"/start"))
            results.append(article)
        count = 0
        for film in films_list:
            count += 1 
            if count == 29:
                break
            data = films_db.get_film_data(film)
            name = data.get("name","0")
            code = data.get("code","0")
            quality = data.get("quality","0")
            size = data.get("size","0")
            views = views_db.get_views_film(code=code)
            if quality == "0" or quality==None:
                title = f"{name}"
            else:
                title = f"{name}, {quality}p"

            article = InlineQueryResultArticle(
        id=code,
        # photo_url="https://i.imgur.com/2HEaBZj.jpg",
        thumb_url="https://i.imgur.com/RxbHv6V.jpg",
        title=title,
        description=f"📁 Hajmi: {size}\n👁Ko'rishlar: {views}",
        input_message_content=InputTextMessageContent(f"/search {code}"))
            results.append(article)
    else:
        films_list = films_db.search_film_data(name=query_text)
        if len(films_list) < 1:
            article = InlineQueryResultArticle(
        id=1,
        title=f"😔 Hech qanday kino topilmadi ...",
        input_message_content=InputTextMessageContent(f"/start"))
            results.append(article)
        count = 0
        for film in films_list:
            count += 1 
            if count == 29:
                break
            name = film[0]
            quality = film[1]
            code = film[2]
            size = film[3]
            views = views_db.get_views_film(code=code)
            

            if quality == "0" or quality==None:
                quality = ""
                title = f"{name}"
            else:
                title = f"{name}, {quality}p"
            article = InlineQueryResultArticle(
        id=code,
        thumb_url="https://i.imgur.com/RxbHv6V.jpg",
        title=title,
        description=f"📁 Hajmi: {size}\n👁Ko'rishlar: {views}",
        input_message_content=InputTextMessageContent(f"/search {code}"))
            results.append(article)

    await bot.answer_inline_query(query.id,results,cache_time=5)

@dp.callback_query_handler(text="refresh")
async def async_function(call: types.CallbackQuery,state: FSMContext):
    try:
        films_list = views_db.get_top_films()
        count = 0
        text = "<b>🏆Top 5:</b>\n\n"
        keyboards = InlineKeyboardMarkup(row_width=3)
        for film in films_list:
            count+=1
            code = film[0]
            data = films_db.get_film_data(code)
            name = data.get("name","0")
            views = views_db.get_views_film(code=code)
            text += f"        {count}. <b>{name} 👁{views}</b>\n"
            keyboards.insert(InlineKeyboardButton(f"{count}",callback_data=f"search:{code}"))
        keyboards.add(InlineKeyboardButton(text="♻️ Yangilash", callback_data='refresh'))
        keyboards.add(InlineKeyboardButton(text="◀️ Ortga", callback_data='user_back'))
        await call.message.edit_text(text,reply_markup=keyboards)
    except:
        await call.answer("❌ Hech qanday ma'lumot o'zgarmadi!")
@dp.callback_query_handler(text="top5")
async def async_function(call: types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    films_list = views_db.get_top_films()
    count = 0
    text = "<b>🏆Top 5:</b>\n\n"
    keyboards = InlineKeyboardMarkup(row_width=3)
    for film in films_list:
        count+=1
        code = film[0]
        data = films_db.get_film_data(code)
        name = data.get("name","0")
        views = views_db.get_views_film(code=code)
        text += f"        {count}. <b>{name} 👁{views}</b>\n"
        keyboards.insert(InlineKeyboardButton(f"{count}",callback_data=f"search:{code}"))
    keyboards.add(InlineKeyboardButton(text="♻️ Yangilash", callback_data='refresh'))
    keyboards.add(InlineKeyboardButton(text="◀️ Ortga", callback_data='user_back'))
    await call.message.answer(text,reply_markup=keyboards)
@dp.callback_query_handler(text_contains="search")
async def async_function(call: types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    kino_kod = call.data.replace("search:","")
    user_id = call.from_user.id
    data = films_db.get_film_data(kino_kod)
    caption = ""
    if not(films_db.check_film_code(kino_kod)):
        msg = await call.message.answer("😔Afsus bunday kino kodi topilmadi!\n\n\n♻️Qaytadan urinib ko'ring",reply_markup=back_user)
        return
    views_db.update_views_film(code=kino_kod,user=user_id)
    if saved_films.check_saved_movie(user=user_id,code=kino_kod):
        text_name = "❌O'chirish(Saqlanganlardan)"
        callback = f"delete:{kino_kod}"
    else:
        text_name = "✔️Saqlash(Saqlanganlarga)"
        callback = f"save:{kino_kod}"

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
            InlineKeyboardMarkup(text = text_name,callback_data=callback),
        ],
        [
            InlineKeyboardMarkup(text = "🏆 Top 5 kinolar",callback_data="top5"),

            InlineKeyboardMarkup(text = "🔍 Kod orqali qidirish",callback_data="film_with_code_"),

        ]    
])

    name = data.get("name","0")
    file_id = data.get("file_id","0")
    code = data.get("code","0")
    genre = data.get("genre","0")
    continuity = data.get("continuity","0")
    author = data.get("author","0")
    language = data.get("language","0")
    quality = data.get("quality","0")
    size = data.get("size","0")
    from_country = data.get("from_country","0")
    views = views_db.get_views_film(code=code)
    if name != "0" and name != None:caption+= f"<b>🎬 Nomi:</b> {name}\n➖➖➖➖➖➖➖\n"
    caption += f"<b>👁 Ko'rishlar soni:</b> {views}\n"
    if continuity != "0" and continuity!= None:caption += f"<b>⏰ Davomiylik:</b> {continuity}\n"
    if from_country != "0" and from_country!= None:caption += f"<b>🌐 Davlat:</b> {from_country}\n"
    if size != "0" and size!= None:caption += f"<b>📁 Hajmi:</b> {size}\n"
    if quality != "0" and quality!= None:caption += f"<b>💿 Sifat:</b> {quality}p\n"
    if genre != "0" and genre != None:caption += f"<b>🎭 Janr:</b> {genre}\n"
    if language != "0" and language!= None:caption += f"<b>🚩 Til:</b> {language}\n\n"
    caption+=f"""<b>🔑 Film kodi:</b> <code>{kino_kod}</code>\n<b>🤖 Bot:</b> @SaraFilmUzBot\n\n\n<b>🍿 @SaraFilmUz - Eng Sara Filmlar</b>"""
    await call.message.answer_video(file_id,caption=caption,reply_markup=keyboards)
@dp.callback_query_handler(text="random")
async def async_function(call: types.CallbackQuery,state: FSMContext):
    await call.message.delete()

    kino_kod = films_db.get_random_film()
    user_id = call.from_user.id
    data = films_db.get_film_data(code=kino_kod)
    views_db.update_views_film(code=kino_kod,user=user_id)
    if saved_films.check_saved_movie(user=user_id,code=kino_kod):
        text_name = "❌O'chirish(Saqlanganlardan)"
        callback = f"delete:{kino_kod}"
    else:
        text_name = "✔️Saqlash(Saqlanganlarga)"
        callback = f"save:{kino_kod}"

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
            InlineKeyboardMarkup(text = text_name,callback_data=callback),
        ],
        [
            InlineKeyboardMarkup(text = "🏆 Top 5 kinolar",callback_data="top5"),
            InlineKeyboardMarkup(text = "🔍 Kod orqali qidirish",callback_data="film_with_code_"),

        ]   
])

    name = data.get("name","0")
    file_id = data.get("file_id","0")
    code = data.get("code","0")
    genre = data.get("genre","0")
    continuity = data.get("continuity","0")
    author = data.get("author","0")
    language = data.get("language","0")
    quality = data.get("quality","0")
    size = data.get("size","0")
    from_country = data.get("from_country","0")
    views = views_db.get_views_film(code=code)
    caption = ""
    if name != "0" and name != None:caption+= f"<b>🎬 Nomi:</b> {name}\n➖➖➖➖➖➖➖\n"
    caption += f"<b>👁 Ko'rishlar soni:</b> {views}\n"
    if continuity != "0" and continuity!= None:caption += f"<b>⏰ Davomiylik:</b> {continuity}\n"
    if from_country != "0" and from_country!= None:caption += f"<b>🌐 Davlat:</b> {from_country}\n"
    if size != "0" and size!= None:caption += f"<b>📁 Hajmi:</b> {size}\n"
    if quality != "0" and quality!= None:caption += f"<b>💿 Sifat:</b> {quality}p\n"
    if genre != "0" and genre != None:caption += f"<b>🎭 Janr:</b> {genre}\n"
    if language != "0" and language!= None:caption += f"<b>🚩 Til:</b> {language}\n\n"
    caption+=f"""<b>🔑 Film kodi:</b> <code>{kino_kod}</code>\n<b>🤖 Bot:</b> @SaraFilmUzBot\n\n\n<b>🍿 @SaraFilmUz - Eng Sara Filmlar</b>"""
    await call.message.answer_video(file_id,caption=caption,reply_markup=keyboards)


@dp.callback_query_handler(text="film___")
async def async_function(call: types.CallbackQuery,state: FSMContext):
    
    msg = await call.message.edit_text("""
<b>🔰 Kino kodini kiriting</b>


<i>❗️Eslatma: 🎥Kino kodlarini @SaraFilmUz kanalidan olishingiz mumkin(Inline Rejimda kinoni nomi bilan ham topishingiz mumkin)!</i>
""",reply_markup=back_user)

    await state.update_data({f"{call.from_user.id}":f"{msg.message_id}"})
    await state.set_state("get_film_code")
@dp.callback_query_handler(state="*",text="user_back")
async def async_function(call: types.CallbackQuery,state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer(text = f"<b>Assalomu alaykum {call.from_user.get_mention()}, botimizga xush kelibsiz</b>\n\n"
             f"🎥 Bot orqali siz sevimli filmlar, seriallar va multfilmlarni sifatli formatda ko'rishingiz mumkin\n\n"
             f"<b>Quyidagi menudan kerakli bo'limni tanlang👇</b>",reply_markup=keyboards)
@dp.callback_query_handler(text="film_with_code_")
async def async_function(call: types.CallbackQuery,state: FSMContext):
    await call.message.delete()
    msg = await call.message.answer("""
<b>🔰 Kino kodini kiriting</b>


<i>❗️Eslatma: 🎥Kino kodlarini @SaraFilmUz kanalidan olishingiz mumkin(Inline Rejimda kinoni nomi bilan ham topishingiz mumkin)!</i>
""",reply_markup=back_user)

    await state.update_data({f"{call.from_user.id}":f"{msg.message_id}"})
    await state.set_state("get_film_code")
@dp.message_handler(state="get_film_code")
async def send_film(message: types.Message,state:FSMContext):
    await message.delete()
    user_id = message.from_user.id
    state_data = await state.get_data()
    msg_id = state_data.get(f"{user_id}")
    try:await bot.delete_message(chat_id=user_id,message_id=msg_id)
    except:pass
    kino_kod = message.text
    user_id = message.from_user.id
    data = films_db.get_film_data(kino_kod)
    caption = ""
    if not(films_db.check_film_code(kino_kod)):
        msg = await message.answer("<b>😔Afsus bunday kino kodi topilmadi!</b>\n\n\n<i>♻️Qaytadan urinib ko'ring</i>",reply_markup=back_user)
        await state.update_data({f"{message.from_user.id}":f"{msg.message_id}"})
        await state.set_state("get_film_code")
        return

    await state.finish()
    views_db.update_views_film(code=kino_kod,user=user_id)
    if saved_films.check_saved_movie(user=user_id,code=kino_kod):
        text_name = "❌O'chirish(Saqlanganlardan)"
        callback = f"delete:{kino_kod}"
    else:
        text_name = "✔️Saqlash(Saqlanganlarga)"
        callback = f"save:{kino_kod}"

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
            InlineKeyboardMarkup(text = text_name,callback_data=callback),
        ],
        [
            InlineKeyboardMarkup(text = "🏆 Top 5 kinolar",callback_data="top5"),
            InlineKeyboardMarkup(text = "🔍 Kod orqali qidirish",callback_data="film_with_code_"),

        ],    
])

    name = data.get("name","0")
    file_id = data.get("file_id","0")
    code = data.get("code","0")
    genre = data.get("genre","0")
    continuity = data.get("continuity","0")
    author = data.get("author","0")
    language = data.get("language","0")
    quality = data.get("quality","0")
    size = data.get("size","0")
    from_country = data.get("from_country","0")
    views = views_db.get_views_film(code=code)
    if name != "0" and name != None:caption+= f"<b>🎬 Nomi:</b> {name}\n➖➖➖➖➖➖➖\n"
    caption += f"<b>👁 Ko'rishlar soni:</b> {views}\n"
    if continuity != "0" and continuity!= None:caption += f"<b>⏰ Davomiylik:</b> {continuity}\n"
    if from_country != "0" and from_country!= None:caption += f"<b>🌐 Davlat:</b> {from_country}\n"
    if size != "0" and size!= None:caption += f"<b>📁 Hajmi:</b> {size}\n"
    if quality != "0" and quality!= None:caption += f"<b>💿 Sifat:</b> {quality}p\n"
    if genre != "0" and genre != None:caption += f"<b>🎭 Janr:</b> {genre}\n"
    if language != "0" and language!= None:caption += f"<b>🚩 Til:</b> {language}\n\n"
    caption+=f"""<b>🔑 Film kodi:</b> <code>{kino_kod}</code>\n<b>🤖 Bot:</b> @SaraFilmUzBot\n\n\n<b>🍿 @SaraFilmUz - Eng Sara Filmlar</b>"""
    await message.answer_video(file_id,caption=caption,reply_markup=keyboards)



@dp.callback_query_handler(text_contains="delete")
async def async_function(call: types.CallbackQuery):
    kino_kod = call.data.split(":")[1]
    user_id = call.from_user.id
    saved_films.delete_saved_movie(user=user_id,code=kino_kod)
    if saved_films.check_saved_movie(user=user_id,code=kino_kod):
        text_name = "❌O'chirish(Saqlanganlardan)"
        callback = f"delete:{kino_kod}"
    else:
        text_name = "✔️Saqlash(Saqlanganlarga)"
        callback = f"save:{kino_kod}"

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
            InlineKeyboardMarkup(text = text_name,callback_data=callback),
        ],
        [
            InlineKeyboardMarkup(text = "🏆 Top 5 kinolar",callback_data="top5"),

            InlineKeyboardMarkup(text = "🔍 Kod orqali qidirish",callback_data="film_with_code_"),

        ]      
])
    await call.message.edit_reply_markup(reply_markup=keyboards)

@dp.callback_query_handler(text_contains="save")
async def async_function(call: types.CallbackQuery):
    kino_kod = call.data.split(":")[1]
    user_id = call.from_user.id
    saved_films.add_saved_movie(user=user_id,code=kino_kod)
    if saved_films.check_saved_movie(user=user_id,code=kino_kod):
        text_name = "❌O'chirish(Saqlanganlardan)"
        callback = f"delete:{kino_kod}"
    else:
        text_name = "✔️Saqlash(Saqlanganlarga)"
        callback = f"save:{kino_kod}"

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
            InlineKeyboardMarkup(text = text_name,callback_data=callback),
        ],
        [
            InlineKeyboardMarkup(text = "🏆 Top 5 kinolar",callback_data="top5"),

            InlineKeyboardMarkup(text = "🔍 Kod orqali qidirish",callback_data="film_with_code_"),

        ]     
])
    await call.message.edit_reply_markup(reply_markup=keyboards)
@dp.message_handler(commands  = ["search"])
async def send_film(message: types.Message):
    await message.delete()
    user_id = message.from_user.id
    kino_kod = message.get_args()
    user_id = message.from_user.id
    data = films_db.get_film_data(kino_kod)
    caption = ""
    if not(films_db.check_film_code(kino_kod)):
        msg = await message.answer("😔Afsus bunday kino kodi topilmadi!\n\n\n♻️Qaytadan urinib ko'ring",reply_markup=back_user)
        return
    views_db.update_views_film(code=kino_kod,user=user_id)
    if saved_films.check_saved_movie(user=user_id,code=kino_kod):
        text_name = "❌O'chirish(Saqlanganlardan)"
        callback = f"delete:{kino_kod}"
    else:
        text_name = "✔️Saqlash(Saqlanganlarga)"
        callback = f"save:{kino_kod}"

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
            InlineKeyboardMarkup(text = text_name,callback_data=callback),
        ],
        [
            InlineKeyboardMarkup(text = "🏆 Top 5 kinolar",callback_data="top5"),

            InlineKeyboardMarkup(text = "🔍 Kod orqali qidirish",callback_data="film_with_code_"),

        ]     
])

    name = data.get("name","0")
    file_id = data.get("file_id","0")
    code = data.get("code","0")
    genre = data.get("genre","0")
    continuity = data.get("continuity","0")
    author = data.get("author","0")
    language = data.get("language","0")
    quality = data.get("quality","0")
    size = data.get("size","0")
    from_country = data.get("from_country","0")
    views = views_db.get_views_film(code=code)
    if name != "0" and name != None:caption+= f"<b>🎬 Nomi:</b> {name}\n➖➖➖➖➖➖➖\n"
    caption += f"<b>👁 Ko'rishlar soni:</b> {views}\n"
    if continuity != "0" and continuity!= None:caption += f"<b>⏰ Davomiylik:</b> {continuity}\n"
    if from_country != "0" and from_country!= None:caption += f"<b>🌐 Davlat:</b> {from_country}\n"
    if size != "0" and size!= None:caption += f"<b>📁 Hajmi:</b> {size}\n"
    if quality != "0" and quality!= None:caption += f"<b>💿 Sifat:</b> {quality}p\n"
    if genre != "0" and genre != None:caption += f"<b>🎭 Janr:</b> {genre}\n"
    if language != "0" and language!= None:caption += f"<b>🚩 Til:</b> {language}\n\n"
    caption+=f"""<b>🔑 Film kodi: </b><code>{kino_kod}</code>\n<b>🤖 Bot:</b> @SaraFilmUzBot\n\n\n<b>🍿 @SaraFilmUz - Eng Sara Filmlar</b>"""
    await message.answer_video(file_id,caption=caption,reply_markup=keyboards)
@dp.message_handler(text="📚 Qo'llanma")
async def qollanma(message: types.Message):
    await message.answer("<b>📚 Botdan foydalanish qo'llanmasi</b>\n\n\n"
                         "1️⃣ <i>@SaraFilmUz</i> kanaliga obuna bo'ling\n\n"
                         "2️⃣ Ko'rmoqchi bo'lgan kino kodini nusxalab oling\n\n"
                         "3️⃣ Botga kirib «🔍Kino izlash» tugmasini bosing\n\n"
                         "4️⃣ Kanaldan nusxalab olgan kino kodini kiriting\n\n"
                         "5️⃣ Kod mavjud bolsa bot sizga uni tashlab beradi\n"
                         "➖➖➖➖➖➖➖\n"
                         "📣 Botga yoki kanalga reklama bermoqchimisiz?\n"
                         "🔗 @OnlyAds_Uz kanaliga kirib reklama tariflarini ko'rib chiqing undan so'ng esa adminga murojaat qiling")
    