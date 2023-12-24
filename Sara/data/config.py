from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = "6357479039:AAEXJc0lK9lhi18TE1QiEALGz6Er9xIcPS0"  # Bot toekn
ADMINS = ["6011359652","6466101131"]  # adminlar ro'yxati
IP = "localhost" # Xosting ip manzili
# from environs import Env

# # environs kutubxonasidan foydalanish
# env = Env()
# env.read_env()

# # .env fayl ichidan quyidagilarni o'qiymiz
# BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
# ADMINS = env.list("ADMINS")  # adminlar ro'yxati
# IP = env.str("ip")  # Xosting ip manzili