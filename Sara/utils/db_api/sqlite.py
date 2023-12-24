from random import choice
import sqlite3
from datetime import datetime
class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id int NOT NULL,
            fullname varchar(255) NOT NULL,
            username varchar(255),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, fullname: str, username: str):
        sql = """
        INSERT INTO Users(id, fullname, username) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, fullname, username), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


class Films:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS films (
                code TEXT,
                file_id TEXT,
                name TEXT,
                genre TEXT,
                continuity TEXT,
                author TEXT,
                language TEXT,
                quality TEXT,
                size TEXT,
                from_country TEXT,
                views INTEGER DEFAULT 0,
                allow_code TEXT
            )
        ''')
        self.conn.commit()
    def save_film(self, code, file_id,name=False, genre=False, continuity=False, author=False, lang=False, quality=False, size=False, from_country=False):
        views = 0
        allow_code = "Allow code"
        self.cursor.execute("SELECT code FROM films WHERE code = ?", (code,))
        result = self.cursor.fetchone()
        if result:
            raise TypeError("Film with the same code already exists")

        self.cursor.execute("INSERT INTO films VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)",
                            (code, file_id, name, genre, continuity, author, lang, quality, size, from_country, views, allow_code))
        self.conn.commit()

    def get_film_code(self, name):
        self.cursor.execute("SELECT code FROM films WHERE name LIKE ?", (f"%{name}%",))
        result = self.cursor.fetchall()
        return [row[0] for row in result]

    def get_film_name(self, code):
        self.cursor.execute("SELECT name FROM films WHERE code LIKE ?", (f"%{code}%",))
        result = self.cursor.fetchall()
        return [row[0] for row in result]
    def search_film_data(self,name):
        self.cursor.execute("SELECT code FROM films WHERE name LIKE ?", (f"%{name}%",))
        result = self.cursor.fetchall()
        codes = [row[0] for row in result]
        my_list = []
        
        for code in codes:
            self.cursor.execute("SELECT name, quality, code, size, views FROM films WHERE code = ?", (code,))
            data = self.cursor.fetchall()
            my_list.append(data[0])
        return my_list
    def get_film_fileid(self, code):
        self.cursor.execute("SELECT file_id FROM films WHERE code = ?", (code,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_views(self, code, allow_code):
        self.cursor.execute("SELECT allow_code FROM films WHERE code = ?", (code,))
        result = self.cursor.fetchone()

        if result and result[0] == allow_code:
            return False

        self.cursor.execute("UPDATE films SET views = views + 1, allow_code = ? WHERE code = ?", (allow_code, code))
        self.conn.commit()
        return True

    def get_film_data(self, code):
        self.cursor.execute("SELECT * FROM films WHERE code = ?", (code,))
        result = self.cursor.fetchone()
        columns = [column[0] for column in self.cursor.description]
        return dict(zip(columns, result)) if result else None

    def get_film_with_name(self, name):
        self.cursor.execute("SELECT code FROM films WHERE name LIKE ?", (f"%{name}%",))
        result = self.cursor.fetchall()
        return [row[0] for row in result]

    def get_film_with_code(self, code):
        self.cursor.execute("SELECT * FROM films WHERE code = ?", (code,))
        result = self.cursor.fetchall()
        return result
    def get_random_film(self):
        films_list = self.get_films_data()
        kino =  choice(films_list)
        kod = kino[2]
        return kod
    def get_films_data(self):
        self.cursor.execute("SELECT name, quality, code, size, views FROM films")
        result = self.cursor.fetchall()
        return result
    def get_top_films(self,limit=3):
        self.cursor.execute("SELECT code FROM films ORDER BY views DESC LIMIT 3")
        result = self.cursor.fetchall()
        return [row[0] for row in result]
    def get_views_film(self, code):
        self.cursor.execute("SELECT views FROM films WHERE code = ?", (code,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    def check_film_code(self, code):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM films WHERE code = ? LIMIT 1)", (code,))
        result = self.cursor.fetchone()
        return bool(result[0])
    def delete_film(self, code):
        self.cursor.execute("SELECT code FROM films WHERE code = ?", (code,))
        result = self.cursor.fetchone()

        if result:
            self.cursor.execute("DELETE FROM films WHERE code = ?", (code,))
            self.conn.commit()
            return True
        else:
            return False

class SavedFilms:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS saved_movies
                            (user TEXT, code TEXT)''')

    def add_saved_movie(self, user, code):
        self.cursor.execute("INSERT INTO saved_movies VALUES (?, ?)", (user, code))
        self.conn.commit()

    def delete_saved_movie(self, user, code):
        self.cursor.execute("DELETE FROM saved_movies WHERE user=? AND code=?", (user, code))
        self.conn.commit()
    def check_saved_movie(self, user, code):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM saved_movies WHERE user=? AND code=?)", (user, code))
        result = self.cursor.fetchone()[0]
        return bool(result)
    def get_saved_movies(self, user):
        self.cursor.execute("SELECT code FROM saved_movies WHERE user=?", (user,))
        saved_movies = self.cursor.fetchall()
        return [movie[0] for movie in saved_movies]
class FilmViewsCount:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def update_views_film(self, code, user):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE code=? AND user=?", (code, user))
        result = self.cursor.fetchone()
        if result[0] == 0:
            self.cursor.execute("INSERT INTO users (code, user) VALUES (?, ?)", (code, user))
            self.conn.commit()

    def get_views_film(self, code):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE code=?", (code,))
        result = self.cursor.fetchone()
        return result[0]

    def get_top_films(self):
        self.cursor.execute("SELECT code, COUNT(*) as user_count FROM users GROUP BY code ORDER BY user_count DESC LIMIT 5")
        result = self.cursor.fetchall()
        return result

    def create_codes_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT,
                user TEXT
            )
        """)
        self.conn.commit()

    def close(self):
        self.conn.close()

class Channel:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS channels
                                (username TEXT PRIMARY KEY,
                                 saved_time TEXT)''')
        self.conn.commit()

    def save_channel(self, username):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO channels VALUES (?, ?)", (username, current_time))
        self.conn.commit()

    def get_channels(self):
        self.cursor.execute("SELECT username FROM channels")
        return [row[0] for row in self.cursor.fetchall()]

    def get_time_channel(self, username):
        self.cursor.execute("SELECT saved_time FROM channels WHERE username=?", (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def del_channel(self, username):
        self.cursor.execute("SELECT username FROM channels WHERE username=?", (username,))
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute("DELETE FROM channels WHERE username=?", (username,))
            self.conn.commit()
            return True
        else:
            return False
        

    def del_channels(self):
        self.cursor.execute("DELETE FROM channels")
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

class BanUser:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT)")
        self.conn.commit()
    def get_ban_users(self):
        self.cursor.execute("SELECT user_id FROM users")
        return [row[0] for row in self.cursor.fetchall()]
    def ban_user(self, user_id):
        self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        self.conn.commit()

    def check_user(self, user_id):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] > 0

    def del_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        self.conn.commit()

        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def del_users(self):
        self.cursor.execute("DELETE FROM users")
        self.conn.commit()

    def get_user(self, place):
        self.cursor.execute("SELECT user_id FROM users ORDER BY ROWID ASC LIMIT 1 OFFSET ?", (place - 1,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def count_users(self):
        self.cursor.execute("SELECT COUNT(*) FROM users")
        result = self.cursor.fetchone()
        return result[0]

    def __del__(self):
        self.cursor.close()
        self.conn.close()

