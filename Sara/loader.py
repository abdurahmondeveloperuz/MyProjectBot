from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.sqlite import Database,Channel,BanUser,Films, SavedFilms, FilmViewsCount

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db='data/main.db')
channels = Channel("data/main.db")
banuser = BanUser("main.db")
films_db = Films("data/films.db")
saved_films = SavedFilms("data/saved_films.db")
views_db = FilmViewsCount("data/views.db")

# print(views_db.get_top_films())
# saved_films.add_saved_movie(user="6466101131",code=1)
# print(films_db.save_film(code="6",file_id="BAACAgQAAxkBAAIkf2V1Z_zaXjwx2snwJaTbhCCy1U7AAAJsCgACsiWpUNF85LJyy5iGMwQ",continuity="02:27:48",genre="#Jangari #Fantastika #Komediya #Sarguzasht",from_country="🇺🇸 AQSH",quality="720",lang="🇺🇿 O'zbek tili(Tarjima)",name="O‘rgimchak Odam 3(Uyga Yo‘l Yo‘q)",size="1909 MB"))
