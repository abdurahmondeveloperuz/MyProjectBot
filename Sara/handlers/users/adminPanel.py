from aiogram.types import Message, CallbackQuery, ContentTypes, InputFile, ChatType
from aiogram.dispatcher import FSMContext
import aiogram
from datetime import datetime
import pytz
import asyncio
import xlsxwriter as xl
import os
from data.config import ADMINS
from keyboards.inline.admin_keys import AdminPanel, SendAd_Type, GoToAdminPanel, backDelete, DeleteUsers, BaseType, \
    answer_admin, back_user
from states.states import send_forwad, sendAd, verifyDeleteUsers, send_user, answer
from loader import dp, db, bot, channels, banuser, films_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.main_keyboards import about_film_keyboards,accept_button
@dp.message_handler(state='*', text="/admin", user_id=ADMINS)
async def adminPanelfunc(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Assalomu alaykum {message.from_user.full_name} Admin Panelga xush kelibsiz", reply_markup=AdminPanel)
@dp.callback_query_handler(state="*", text='add_kino')
async def addfilm(call: CallbackQuery, state:FSMContext):
    await call.message.delete()
    await call.message.answer("""<b>➕ Kino qo'shish uchun menga qo'shiladigan
🔑 Kino kodini o'ylab topib yuboring!</b>""",reply_markup=GoToAdminPanel)
    await state.set_state("kino_kod_add")


@dp.message_handler(state="kino_kod_add")
async def EnterFilmCode(message: Message,state:FSMContext):
    kino_kod = message.text
    res = films_db.check_film_code(code=kino_kod)
    if res:

        await message.answer("<b>❌ Bunday kod allaqachon mavjud!</b>\n\n\n<i>♻️ Qaytadan kiritib ko'ring!</i>",reply_markup=GoToAdminPanel)
        await state.set_state("kino_kod_add")
    else:
        await message.answer("<b>🔑 Yaxshi kino kodi saqlandi</b>\n\n\n<i> 🎬 Endi menga kino nomini yuboring!</i>",reply_markup=GoToAdminPanel)
        await state.update_data({f"{message.from_user.id}_kod":message.text})
        await state.set_state("enter_film_name")
@dp.message_handler(state="enter_film_name")
async def EnterFilmCode(message: Message,state:FSMContext):
    kino_nom = message.text
    await message.answer("<b>🎬 Yaxshi kino nomi saqlandi</b>\n\n\n<i>🎥 Endi menga kinoni yuboring!</i>",reply_markup=GoToAdminPanel)
    await state.update_data({f"{message.from_user.id}_name":kino_nom})
    await state.set_state("enter_film")
@dp.message_handler(state="enter_film",content_types=["video"])
async def EnterFilmsData(message: Message,state:FSMContext):
    await message.answer("<b>🎥 Kino saqlandi!\n📂 Endi menga kinoga tegishli ma'lumotlarni\n📩 Mavjudlarini kiriting</b>\n\n\n<i>📌 Kiritishda tugmalardan foydalaning</i>",reply_markup=about_film_keyboards)
    file_id = message.video.file_id
    await state.update_data({f"{message.from_user.id}_FileId":file_id})
    await state.set_state("films_data")

@dp.callback_query_handler(state='films_data', text='country')
async def EnterName(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("🌐 Kino ishlab chiqarilgan davlatni kiriting:",reply_markup=GoToAdminPanel)
    await state.set_state('films_country')

@dp.message_handler(state='films_country')
async def adminPanelfunc(message: Message, state: FSMContext):
    country = message.text
    await state.update_data({f"{message.from_user.id}_country":country})
    await message.answer("""<b>
🌐 Kino ishlab chiqarilgan davlat saqlandi</b>""",reply_markup=about_film_keyboards)
    await state.set_state("films_data")
@dp.callback_query_handler(state='films_data', text='language')
async def EnterName(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("🚩 Kinoni tilini kiriting:",reply_markup=GoToAdminPanel)
    await state.set_state('films_language')

@dp.message_handler(state='films_language')
async def adminPanelfunc(message: Message, state: FSMContext):
    language = message.text
    await state.update_data({f"{message.from_user.id}_language":language})
    await message.answer("""<b>
🚩Kino tili saqlandi</b>""",reply_markup=about_film_keyboards)
    await state.set_state("films_data")

@dp.callback_query_handler(state='films_data', text='quality')
async def EnterName(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("💿 Kinoni sifatini kiriting:",reply_markup=GoToAdminPanel)
    await state.set_state('films_quality')

@dp.message_handler(state='films_quality')
async def adminPanelfunc(message: Message, state: FSMContext):
    quality = message.text
    await state.update_data({f"{message.from_user.id}_quality":quality})
    await message.answer("""<b>
💿 Kino sifati saqlandi</b>""",reply_markup=about_film_keyboards)
    await state.set_state("films_data")
@dp.callback_query_handler(state='films_data', text='continuity')
async def EnterName(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("⏰ Kino davomiyligini kiriting:",reply_markup=GoToAdminPanel)
    await state.set_state('films_continuity')

@dp.message_handler(state='films_continuity')
async def adminPanelfunc(message: Message, state: FSMContext):
    continuity = message.text
    await state.update_data({f"{message.from_user.id}_continuity":continuity})
    await message.answer("<b>⏰ Kino davomiyligi saqlandi</b>",reply_markup=about_film_keyboards)
    await state.set_state("films_data")
@dp.callback_query_handler(state='films_data', text='size')
async def EnterName(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("📁 Kino hajmini kiriting:",reply_markup=GoToAdminPanel)
    await state.set_state('films_size')

@dp.message_handler(state='films_size')
async def adminPanelfunc(message: Message, state: FSMContext):
    size = message.text
    await state.update_data({f"{message.from_user.id}_size":size})
    await message.answer("""<b>
📁 Kino hajmi saqlandi</b>""",reply_markup=about_film_keyboards)
    await state.set_state("films_data")
@dp.callback_query_handler(state='films_data', text='genre')
async def EnterName(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("🎭 Kino janrini kiriting:",reply_markup=GoToAdminPanel)
    await state.set_state('films_genre')

@dp.message_handler(state='films_genre')
async def adminPanelfunc(message: Message, state: FSMContext):
    genre = message.text
    await state.update_data({f"{message.from_user.id}_genre":genre})
    await message.answer("""<b>
🎭 Kino janri saqlandi</b>""",reply_markup=about_film_keyboards)
    await state.set_state("films_data")
@dp.callback_query_handler(state='films_data', text='past')
async def EnterName(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    state_data = await state.get_data()
    kino_file_id = state_data.get(f"{call.from_user.id}_FileId")
    name = state_data.get(f"{call.from_user.id}_name")
    country = state_data.get(f"{call.from_user.id}_country")
    language = state_data.get(f"{call.from_user.id}_language")
    quality = state_data.get(f"{call.from_user.id}_quality")
    continuity = state_data.get(f"{call.from_user.id}_continuity")
    genre = state_data.get(f"{call.from_user.id}_genre")
    size = state_data.get(f"{call.from_user.id}_size")
    kino_kod = state_data.get(f"{call.from_user.id}_kod")
    caption = ""
    if name:caption+=f"<b>🎬 Nomi:</b> {name}\n➖➖➖➖➖➖➖\n"
    if country:caption+=f"<b>🌐 Davlat: </b>{country}\n"           
    if language:caption+=f"<b>🚩 Til: </b>{language}\n"
    if quality:caption+=f"<b>💿 Sifat:</b> {quality}\n"
    if size:caption += f"<b>📀 Hajmi: </b>{size}\n"
    if continuity:caption+=f"<b>⏰ Davomkiylik: </b>{continuity}\n"
    if genre:caption+=f"<b>🎭 Janr:</b> {genre}\n\n"
    caption+=f"""<b>🔑 Film kodi:</b> <code>{kino_kod}</code>\n<b>🤖 Bot:</b> @SaraFilmUzBot\n\n\n<b>🍿 @SaraFilmUz - Eng Sara Filmlar</b>"""
    await call.message.answer_video(kino_file_id,caption=caption,reply_markup=accept_button)
    await state.set_state("accept_button")
@dp.callback_query_handler(state="accept_button",text="accept")
async def adminPanelfunc(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    state_data = await state.get_data()
    kino_file_id = state_data.get(f"{call.from_user.id}_FileId")
    name = state_data.get(f"{call.from_user.id}_name")
    country = state_data.get(f"{call.from_user.id}_country")
    language = state_data.get(f"{call.from_user.id}_language")
    quality = state_data.get(f"{call.from_user.id}_quality")
    continuity = state_data.get(f"{call.from_user.id}_continuity")
    genre = state_data.get(f"{call.from_user.id}_genre")
    size = state_data.get(f"{call.from_user.id}_size")
    kino_kod = state_data.get(f"{call.from_user.id}_kod")
    caption = ""
    if name:caption+=f"<b>🎬 Nomi:</b> {name}\n➖➖➖➖➖➖➖\n"
    if country:caption+=f"<b>🌐 Davlat: </b>{country}\n"          
    if language:caption+=f"<b>🚩 Til: </b>{language}\n"
    if quality:caption+=f"<b>💿 Sifat:</b> {quality}\n"
    if size:caption += f"<b>📀 Hajmi: </b>{size}\n"
    if continuity:caption+=f"<b>⏰ Davomkiylik: </b>{continuity}\n"
    if genre:caption+=f"<b>🎭 Janr:</b> {genre}\n\n"
    caption+=f"""<b>🔑 Film kodi:</b> <code>{kino_kod}</code>\n<b>🤖 Bot:</b> @SaraFilmUzBot\n\n\n<b>🍿 @SaraFilmUz - Eng Sara Filmlar</b>\n"""
    caption+=f"<b>✅Kino tasdiqlandi va kino ro'yhatga qo'shildi</b>"
    try:
        films_db.save_film(code=kino_kod,name=name,genre=genre,file_id=kino_file_id,size=size,continuity=continuity,from_country=country,lang=language,quality=quality)
        await call.message.answer_video(kino_file_id,caption=caption)
    except:
        await call.message.answer("""
❌ Noma'lum xatolik yuz berdi
♻️Qaytadan urunib ko'ring""")
    await state.finish()
    
    

@dp.callback_query_handler(state="*", text='GoToAdminPanel')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Admin Panelga xush kelibsiz", reply_markup=AdminPanel)

@dp.callback_query_handler(state="*", text='admin:block')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    key = InlineKeyboardMarkup(row_width=3)
    if int(banuser.count_users() // 5) == banuser.count_users() / 5:
        users_count = banuser.count_users() // 5
    else:
        users_count = banuser.count_users() // 5 + 1
    all_users = banuser.get_ban_users()
    for i in range(0,5):
        
        try:
            data = await bot.get_chat(all_users[i])
            fullname = data.fullname
            key.add(InlineKeyboardButton(fullname,callback_data=f"user:{all_users[i]}"))
        except:
            try:
                key.add(InlineKeyboardButton(all_users[i],callback_data=f"user:{all_users[i]}"))
            except:
                pass
    if users_count > 1:
        next_ = 2
    else:
        next_ = "no"
    if users_count == 0:
        users_count = 1
    key.add(InlineKeyboardButton("⬅️ Ortga",callback_data=f"previus:no"))
    key.insert(InlineKeyboardButton(f"1/{users_count}",callback_data=f"page_count"))
    key.insert(InlineKeyboardButton("➡️ Oldinga",callback_data=f"next:{next_}"))

    key.add(InlineKeyboardButton("➕ Qo'shish",callback_data=f"admin:add_block_user"))
    key.add(InlineKeyboardButton("🔙 Ortga",callback_data=f"GoToAdminPanel"))
    await call.message.edit_text("Ushbu tugmalar orqali sozlashingiz mumkin!",reply_markup=key)
@dp.callback_query_handler(state="*", text_contains ='admin:add_block_user')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f"🚫Blok qilmoqchi bo'lgan useringizni idsini kiriting: ",reply_markup=GoToAdminPanel)
    await state.set_state("new_block_user")

@dp.message_handler(state="new_block_user")
async def GoAdminPanelf(message: Message, state: FSMContext):
    await state.finish()
    channel = message.text
    try:
        msg = await bot.send_message(chat_id=channel,text=".")
        await msg.delete()
    except:
        await message.answer("<b>❌Botda ushbu foydalanuvchi mavjud emas yoki id notog'ri kiritildi</b>\n\n\n<i>🔁 Qaytadan idni kiritishga urunib ko'ring:</i>",reply_markup=GoToAdminPanel)
        await state.set_state("new_block_user")
    else:
        if not(banuser.check_user(channel)):
            banuser.ban_user(channel)
            await message.answer("<b>✅Foydalanuvchi banlandi.</b>\n\n\n<i>👥Endi ushbu foydalanuvchi botdan foydalanolmaydi</i>")
            await message.answer("Admin Panelga xush kelibsiz!",reply_markup=AdminPanel)
            await state.finish()
        else:
            await message.answer("<b>✅Ushbu foydalanuvchi allaqachon banlangan!</b>")
            await message.answer("Admin Panelga xush kelibsiz!",reply_markup=AdminPanel)
            await state.finish()

@dp.callback_query_handler(state="*", text_contains ='next:')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    next_ = call.data.replace("next:","")
    

    if next_ == "no":
        await call.answer("🔙 Oldinga o'tib bo'lmaydi")
        return
    current = int(next_)

    key = InlineKeyboardMarkup(row_width=3)
    if int(banuser.count_users() // 5) == banuser.count_users() / 5:
        users_count = banuser.count_users() // 5
    else:
        users_count = banuser.count_users() // 5 + 1 

    all_users = banuser.get_ban_users()

    for i in range(int(next_) * 5 - 5,int(next_) * 5):
    
        try:
            data = await bot.get_chat(all_users[i])
            fullname = data.fullname
            key.add(InlineKeyboardButton(fullname,callback_data=f"user:{all_users[i]}"))
        except:
            try:

                key.add(InlineKeyboardButton(all_users[i],callback_data=f"user:{all_users[i]}"))
            except:
                pass
    if users_count <= int(next_):
        next_ = "no"
    else:
        next_ = int(next_) + 1
    if users_count <= 1:
        previus_ = "no"
    else:
        previus_ = current - 1
    key.add(InlineKeyboardButton("⬅️ Ortga",callback_data=f"previus:{previus_}"))
    key.insert(InlineKeyboardButton(f"{current}/{users_count}",callback_data=f"page_count"))
    key.insert(InlineKeyboardButton("➡️ Oldinga",callback_data=f"next:{next_}"))

    key.add(InlineKeyboardButton("➕ Qo'shish",callback_data=f"admin:add_block_user"))
    key.add(InlineKeyboardButton("🔙 Ortga",callback_data=f"GoToAdminPanel"))
    await call.message.edit_text("Ushbu tugmalar orqali sozlashingiz mumkin!",reply_markup=key)

@dp.callback_query_handler(state="*", text_contains ='previus:')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    previus_ = call.data.replace("previus:","")

    if previus_ == "no":
        await call.answer("🔙 Ortga qaytib bo'lmaydi")
        return
    current = int(previus_)
    next_ = current + 1
    key = InlineKeyboardMarkup(row_width=3)
    if int(banuser.count_users() // 5) == banuser.count_users() / 5:
        users_count = banuser.count_users() // 5
    else:
        users_count = banuser.count_users() // 5 + 1
    all_users = banuser.get_ban_users()
    for i in range(int(previus_) * 5 - 5,int(previus_) * 5):
        
        try:
            data = await bot.get_chat(all_users[i])
            key.add(InlineKeyboardButton(data.fullname,callback_data=f"user:{all_users[i]}"))
        except Exception as e:
            print(e)
            key.add(InlineKeyboardButton(all_users[i],callback_data=f"user:{all_users[i]}"))
    if users_count <= int(next_):
        next_ = "no"
    else:
        next_ = current + 1
    if users_count <= 1:
        previus_ = "no"
    else:
        previus_ = int(previus_) - 1
    key.add(InlineKeyboardButton("⬅️ Ortga",callback_data=f"previus:{previus_}"))
    key.insert(InlineKeyboardButton(f"{current}/{users_count}",callback_data=f"page_count"))
    key.insert(InlineKeyboardButton("➡️ Oldinga",callback_data=f"next:{next_}"))

    key.add(InlineKeyboardButton("➕ Qo'shish",callback_data=f"admin:add_block_user"))
    key.add(InlineKeyboardButton("🔙 Ortga",callback_data=f"GoToAdminPanel"))
    await call.message.edit_text("Ushbu tugmalar orqali sozlashingiz mumkin!",reply_markup=key)

@dp.callback_query_handler(state="*", text_contains ='user:')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.data.replace("user:","")
    data = await bot.get_chat(user_id)
    name = data.title
    bio = data.bio
    username = data.username
    id = data.id
    try: 
        txt = await bot.send_message(chat_id=id,text=".")
        await txt.delete()
        bot_blocked = "✅Foydalanuvchi ayni paytda botni bloklamagan"
    except:
        bot_blocked = "❌Foydalanuvchi ayni paytda botni bloklagan"

    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton("➖O'chirib yuborish",callback_data=f"del_ban:{user_id}"))
    btn.add(InlineKeyboardButton(text="🔙 Ortga", callback_data=f'GoToAdminPanel'))

    await call.message.edit_text(f"""
<b>‼️Ushbu foydalanuvchi haqida ma'lumot</b>
    <b>├───📛Foydalanuvchi nomi:</b> {data.full_name} 
    <b>├───🔗Foydalanuvchi useri:</b> @{username}
    <b>├───🆔Foydalanuvchi idsi:</b> <code>{id}</code>
    <b>└───☣️Foydalanuvchi biosi:</b> {bio} 
➖➖➖➖➖➖➖➖➖➖➖
<b>{bot_blocked}</b>
""", reply_markup=btn)
@dp.callback_query_handler(state="*", text_contains ='del_ban:')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    user_id = call.data.replace("del_ban:","")
    if banuser.del_user(user_id):
        await call.message.edit_text(f"""
<b>✅Foydalanuvchi royhatdan muvaffaqiyatli o'chirildi.</b>


<i>🥱Endi ushbu foydalanuvchi botdan foydalanish huquqiga ega!</i>""",reply_markup=GoToAdminPanel)
    else:
        await call.message.edit_text(f"""
<b>❌Foydalanuvchi royhatdan muvaffaqiyatli o'chirilmadi.</b>


<i>🥱Sizdan avvalroq biror bir admin foydalanuvchini ro'yhatdan o'chirib yuborganga o'xshaydi</i>""",reply_markup=GoToAdminPanel)

    
@dp.callback_query_handler(state="*", text_contains ='del_channel:')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    chan_id = call.data.replace("del_channel:","")
    if channels.del_channel(chan_id):
        await call.message.edit_text(f"""
<b>✅Kanal muvaffaqiyatli o'chirildi.</b>


<i>🥱Endi foydalanuvchilar botdan foydalanish uchun bu kanalga obuna bo'lishi shart emas</i>""",reply_markup=GoToAdminPanel)
    else:
        await call.message.edit_text(f"""
<b>❌Kanal muvaffaqiyatli o'chirilmadi.</b>


<i>🥱Sizdan avvalroq biror bir admin kanalni o'chirib yuborganga o'xshaydi</i>""",reply_markup=GoToAdminPanel)

@dp.callback_query_handler(state="*", text_contains ='admin:add_channel')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f"💫Majburiy obunaga qo'ymoqchi bo'lgan kanalingiz userini kiriting: ",reply_markup=GoToAdminPanel)
    await state.set_state("new_channel")

@dp.message_handler(state="new_channel")
async def GoAdminPanelf(message: Message, state: FSMContext):
    await state.finish()
    channel = message.text
    try:
        msg = await bot.send_message(chat_id=channel,text=".")
        await msg.delete()
    except:
        await message.answer("<b>❌Bot kanalda admin emas yoki kanal useri notog'ri kiritildi!</b>\n\n\n<i>👮🏻‍♂️ Botni kanalda admin qilib qaytadan userini kiriting:</i>",reply_markup=GoToAdminPanel)
        await state.set_state("new_channel")
    else:
        try:
            channels.save_channel(channel)
        except:
            await message.answer("✅Ushbu kanal majburiy obunada allaqachon mavjud")
            await message.answer("Admin Panelga xush kelibsiz!",reply_markup=AdminPanel)
            await state.finish()
        else:
            await message.answer("<b>✅Kanal majburiy obunaga qo'shildi.</b>\n\n\n<i>👥Endi barcha foydalanuvchilar botdan foydalanish uchun kanalga obuna bo'lishga majbur</i>")
            await message.answer("Admin Panelga xush kelibsiz!",reply_markup=AdminPanel)
            await state.finish()


@dp.callback_query_handler(state="*", text_contains ='channel:')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    chan_id = call.data.replace("channel:","")
    data = await bot.get_chat(chan_id)
    name = data.title
    bio = data.description
    username = data.username
    members_count = await bot.get_chat_members_count(chat_id=chan_id)
    invite_link = data.invite_link
    id = data.id
    time = channels.get_time_channel(username=chan_id).split(" ")
    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton("➖O'chirib yuborish",callback_data=f"del_channel:{chan_id}"))
    btn.add(InlineKeyboardButton(text="🔙 Ortga", callback_data=f'GoToAdminPanel'))

    await call.message.edit_text(f"""
<b>‼️Ushbu kanal haqida ma'lumot</b>
    <b>├───📛Kanal nomi:</b> {name} 
    <b>├───🔗Kanal useri:</b> @{username}
    <b>├───👥A'zolar soni:</b> {members_count}
    <b>├───🆔Kanal idsi:</b> <code>{id}</code>
    <b>└───☣️Kanal tavfsifi:</b> {bio} 
➖➖➖➖➖➖➖➖➖➖➖
<b>💥Ushbu kanal majburiy obunaga qo'shilgan:
    ├───📅 Sana:</b> {time[0]}<b>
    └───⏰ Vaqt: </b>{time[1]}
""", reply_markup=btn)

@dp.callback_query_handler(state="*", text='admin:channels')
async def GoAdminPanelf(call: CallbackQuery, state: FSMContext):
    await state.finish()
    btn = InlineKeyboardMarkup(row_width=1)
    l_channels = channels.get_channels()
    for channel in l_channels:
        data = await bot.get_chat(channel)
        title = data.title
        btn.add(InlineKeyboardButton(f"{title}",callback_data=f"channel:{channel}"))
    btn.add(InlineKeyboardButton("➕ Qo'shish",callback_data=f"admin:add_channel"))
    btn.add(InlineKeyboardButton("🔙 Ortga",callback_data=f"GoToAdminPanel"))
    await call.message.edit_text("Ushbu tugmalar orqali boshqarishingiz mumkin!", reply_markup=btn)

@dp.callback_query_handler(state='*', text='user_back')
async def user_backfunc(call: CallbackQuery, state: FSMContext):
    await state.finish()


@dp.callback_query_handler(state='*', text='admin:send_ad')
async def send_ad(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Foydalanuvchilarga habar yuborish turini tanlang", reply_markup=SendAd_Type)


@dp.callback_query_handler(state='*', text='forward_habar')
async def forward_habar(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<b>📣 Forward habar yuborishingiz mumkin</b>", reply_markup=GoToAdminPanel)
    await send_forwad.text.set()


@dp.message_handler(state=send_forwad.text, content_types=ContentTypes.ANY)
async def text_forward(message: Message, state: FSMContext):
    await state.finish()
    users = db.select_all_users()
    x = 0
    y = 0
    start = datetime.now(pytz.timezone('Asia/Tashkent'))
    i = await message.answer("🔰 Reklama yuborilmoqda, iltimos biroz kutib turing...")
    for user in users:
        try:
            await bot.forward_message(chat_id=user[0],
                                      from_chat_id=message.from_user.id,
                                      message_id=message.message_id)
            x += 1
        except:
            y += 1
        await asyncio.sleep(0.05)
    finish = datetime.now(pytz.timezone('Asia/Tashkent'))
    farq = finish - start
    await message.answer(f"<b>📣 Reklama yuborildi</b>\n\n"
                         f"✅ Qabul qildi: {x} ta\n"
                         f"❌ Yuborilmadi: {y} ta\n\n"
                         f"<b>⏰ Boshlandi:</b> {start.strftime('%H:%M:%S')}\n"
                         f"<b>⏰ Yakunlandi:</b> {finish.strftime('%H:%M:%S')}\n\n"
                         f"<b>🕓 Umumiy ketgan vaqt:</b> {farq.seconds} soniya", reply_markup=GoToAdminPanel)


@dp.callback_query_handler(state='*', text='oddiy_habar')
async def oddiy_habar(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("""
<b>📣 Reklamani yuborishingiz mumkin</b>


<b>🔑Kalit so'zlar:</b> <i>
    ⏰Vaqt:  <code>{{time}}</code> ushbu xabar foydalanuvchiga borgandagi vaqt bilan xabarni almashtiradi(Misol: 18:39) 
    📅Sana: <code>{{date}}</code> ushbu xabar foydalanuvchiga borgandagi sana bilan xabarni almashtiradi(Misol: 25.11.2023)
    📛Ism: <code>{{name}}</code> ushbu xabarni foydalanuvchi ismi bilan almashtiradi
    🔗Mention: <code>{{mention}}</code> ushbu xabarni foydalanuvchiga havola bilan almashtiradi
    🖇Username: <code>{{username}}</code> ushbu xabarni foydalanuvchi usernami bilan almashtiradi
    🆔 ID: <code>{{id}}</code> ushbu xabarni foydalanuvchi idsi bilan almashtiradi
    👥Foydalanuvchilar: <code>{{users}}</code> ushbu xabarni bazadagi foydalanuvchi soni bilan alishtiradi.
</i>
""", reply_markup=GoToAdminPanel)
    await sendAd.text.set()


@dp.message_handler(state=sendAd.text, content_types=ContentTypes.ANY)
async def rek_text(message: Message, state: FSMContext):
    await state.finish()
    users = db.select_all_users()
    x = 0
    y = 0
    start = datetime.now(pytz.timezone('Asia/Tashkent'))
    i = await message.answer("🔰 Reklama yuborilmoqda, iltimos biroz kutib turing...")
    skip = InlineKeyboardMarkup().add(InlineKeyboardButton("❌", callback_data="skip"))
    count = str(db.count_users())
    for user in users:
        try:
            user_data  = await bot.get_chat(user[0])
            time = datetime.now(pytz.timezone('Asia/Tashkent'))
            ad = message.html_text
            ad = ad.replace("{{time}}",str(time.strftime('%H:%M:%S')))
            ad = ad.replace("{{date}}",str(time.date()))
            ad = ad.replace("{{name}}",str(user_data.full_name))
            ad = ad.replace("{{mention}}",str(user_data.get_mention()))
            ad = ad.replace("{{username}}",str(user_data.username))
            ad = ad.replace("{{id}}",str(user_data.id))
            ad = ad.replace("{{users}}",count[0])
            msg = await bot.send_message(chat_id=user[0],text=ad)
            x += 1
        except Exception as e:
            print(e)
            y += 1
        await asyncio.sleep(0.05)
    finish = datetime.now(pytz.timezone('Asia/Tashkent'))
    farq = finish - start
    await message.answer(f"<b>📣 Reklama yuborildi</b>\n\n"
                         f"✅ Qabul qildi: {x} ta\n"
                         f"❌ Yuborilmadi: {y} ta\n\n"
                         f"<b>⏰ Boshlandi:</b> {start.strftime('%H:%M:%S')}\n"
                         f"<b>⏰ Yakunlandi:</b> {finish.strftime('%H:%M:%S')}\n\n"
                         f"<b>🕓 Umumiy ketgan vaqt:</b> {farq.seconds} soniya", reply_markup=GoToAdminPanel)


@dp.callback_query_handler(state="*", text='admin:bot_stat')
async def bot_stat(call: CallbackQuery, state: FSMContext):
    await state.finish()
    count = db.count_users()[0]
    users = db.select_all_users()
    x = 0
    y = 0
    for user in users:
        try:
            await bot.get_chat(user[0])
            x += 1
        except:
            y += 1
    await call.answer(f"✅ Aktiv: {x}\n"
                      f"❌ Bloklangan: {y}\n"
                      f"➖➖➖➖➖➖\n"
                      f"Umumiy: {count} ta", show_alert=True)


@dp.callback_query_handler(state='*', text='admin:delete_users')
async def delete_users(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<b>✅ Tasdiqlash</b>\n\n"
                                 "Bot foydalanuvchilarini o'chirish uchun tasdiqlash kodini kiriting", reply_markup=GoToAdminPanel)
    await verifyDeleteUsers.code.set()


@dp.message_handler(state=verifyDeleteUsers.code)
async def verifyCode(message: Message):
    if message.text == "8FSD778FSJ":
        await message.answer("Kod to'g'ri. Endi pastdagi tugmani bosish orqali foydalanuvchilarni o'chirishingiz mumkin", reply_markup=DeleteUsers)
    else:
        await message.answer("Kod xato. Qayta urinib ko'ring yoki bekor qiling", reply_markup=backDelete)
        await verifyDeleteUsers.code.set()


@dp.callback_query_handler(state='*', text='delete:verify')
async def deleteVerify(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db.delete_users()
    textm = await call.message.edit_text("✅ Bot foydalanuvchilari o'chirildi")
    await asyncio.sleep(4)
    await textm.edit_text("Admin Panelga xush kelibsiz", reply_markup=AdminPanel)


@dp.callback_query_handler(state='*', text='admin:base')
async def base(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Bazani qaysi turda yuklamoqchisiz", reply_markup=BaseType)


@dp.callback_query_handler(state='*', text='database')
async def database(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    doc = InputFile('data/main.db')
    await call.message.answer_document(document=doc, caption="<b>main.db</b>\n"
                                                             "Baza yuklandi")
    await call.message.answer("Admin Panelga xush kelibsiz", reply_markup=AdminPanel)


@dp.callback_query_handler(state='*', text='excel')
async def excel(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    users = db.select_all_users()
    workbook = xl.Workbook("users.xlsx")
    bold_format = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet("Users")
    worksheet.write('A1', 'ID', bold_format)
    worksheet.write('B1', 'Ism', bold_format)
    worksheet.write('C1', 'Username', bold_format)
    rowIndex = 2
    for user in users:
        tg_id = user[0]
        fullname = user[1]
        username = user[2]

        worksheet.write('A' + str(rowIndex), tg_id)
        worksheet.write('B' + str(rowIndex), fullname)
        worksheet.write('C' + str(rowIndex), f"@{username}")

        rowIndex += 1
    workbook.close()
    file = InputFile(path_or_bytesio="users.xlsx")
    await call.message.answer_document(document=file, caption="<b>users.xlsx</b>\n"
                                                              "Excel formatida")
    os.remove(path="users.xlsx")
    await call.message.answer("Admin Panelga xush kelibsiz", reply_markup=AdminPanel)


@dp.callback_query_handler(state='*', text='admin:send_user')
async def send_user_func(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("<b>🆔 ID</b>\n\n"
                                 "Foydalanuvchi ID sini kiriting", reply_markup=backDelete)
    await send_user.id.set()


@dp.message_handler(state=send_user.id)
async def id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)

    await message.answer(f"<b>📝 XABAR</b>\n\n"
                         f"[<code>{message.text}</code>] ID siga yubormoqchi bo'lgan xabaringizni yuboring",
                         reply_markup=backDelete)
    await send_user.habar.set()


@dp.message_handler(state=send_user.habar)
async def habar(message: Message, state: FSMContext):
    await state.update_data(habar=message.text)

    data = await state.get_data()
    id = data.get('id')
    habar = data.get('habar')
    status = bool
    try:
        await bot.send_message(chat_id=id, text=f"#admin_xabari\n"
                                                f"Sizga admin xabar yubordi\n\n"
                                                f"<b>📝 XABAR:</b> {habar}\n\n"
                                                f"‼️ Agar siz adminga javob yozmoqchi bo'lsangiz quyidagi tugmani bosing👇", reply_markup=answer_admin)
        status = True
    except aiogram.exceptions.ChatNotFound:
        status = False
        await message.answer(f"<b>❌ ID topilmadi</b>\n\n"
                             f"[<code>{id}</code>] ID si topilmadi\n"
                             f"Yoki ushbu foydalanuvchi botda mavjud emas\n\n"
                             f"<i>Boshqa ID yuboring</i>", reply_markup=GoToAdminPanel)
        await send_user.id.set()
    except:
        status = False
        await message.answer(f"<b>❌ Noma'lum xatolik</b>\n\n"
                             f"Qayerdadir xatolik ketdi\n\n"
                             f"<i>Boshq ID yuboring</i>", reply_markup=GoToAdminPanel)
        await send_user.id.set()
    if status:
        await message.answer(f"<b>✅ Yuborildi</b>\n\n"
                             f"ID: [<code>{id}</code>]\n"
                             f"Xabar: {habar}\n\n"
                             f"Xabaringiz muvaffaqiyatli yuborildi")
        await state.finish()
        await message.answer("Admin Panelga xush kelibsiz", reply_markup=AdminPanel)


@dp.callback_query_handler(state='*', text='answer_admin')
async def answeradmin(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f"<b>📝 XABAR</b>\n\n"
                                 f"Adminga yozmoqchi bo'lgan xabaringizni kiriting", reply_markup=back_user)
    await answer.habar.set()


@dp.message_handler(state=answer.habar)
async def adminhabar(message: Message, state: FSMContext):
    await state.finish()
    status = bool
    try:
        status = True
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=f"🆕 Yangi xabar!\n"
                                                       f"🙍🏻‍♂️ ISM: {message.from_user.get_mention()}\n"
                                                       f"⏺ Username: @{message.from_user.username}\n"
                                                       f"🆔 ID: [<code>{message.from_user.id}</code>]\n\n"
                                                       f"📄 Xabar: {message.text}")
    except:
        status = False
    if status:
        await message.answer(f"<b>✅ Yuborildi</b>\n\n"
                             f"Xabar: {message.text}\n\n"
                             f"Xabaringiz muvaffaqiyatli yuborildi")
    else:
        await message.answer("<b>❌ Xatolik</b>\n\n"
                             "Qayerdadir xatolik ketdi", reply_markup=back_user)
