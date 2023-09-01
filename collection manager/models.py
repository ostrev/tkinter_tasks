import random
import sqlite3
from datetime import datetime


class DB:
    def __init__(self):
        self.db_name = "collection_manager.db"
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.db_type = 'games'
        self.create_database()

    def create_database(self):
        create_table_query_movie = """
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            watched_on DATE,
            date DATE,
            genre TEXT,
            director TEXT,
            rating REAL,
            description TEXT
        )
        """
        create_table_query_games = """
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date DATE,
            genre TEXT,
            company TEXT,
            rating REAL,
            description TEXT
        )
        """
        create_table_query_books = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date DATE,
            genre TEXT,
            author TEXT,
            rating REAL,
            description TEXT
        )
        """
        self.cursor.execute(create_table_query_movie)
        self.cursor.execute(create_table_query_games)
        self.cursor.execute(create_table_query_books)
        self.connection.commit()

    def get_items(self, table_name):
        self.db_type = table_name

        query = f"SELECT * FROM {self.db_type}"

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def populate_dummy_games_data(self):
        # Generate and insert dummy data for games
        for _ in range(10):  # Insert 10 dummy games
            game_name = f"Game{random.randint(1, 100)}"
            date = datetime.now().strftime('%Y-%m-%d')
            genre = "Action"
            company = "Dummy Company"
            rating = round(random.uniform(1, 10), 2)
            description = "This is a dummy game."
            args = (game_name, date, genre, company, rating, description)
            self.cursor.execute(
                "INSERT OR IGNORE INTO games (name, date, genre, company, rating, description) VALUES (?, ?, ?, ?, ?, ?)",
                args)
        self.connection.commit()

    def populate_dummy_movies_data(self):
        # Generate and insert dummy data for movies
        for _ in range(10):  # Insert 10 dummy movies
            movie_name = f"Movie{random.randint(1, 100)}"
            watched_on = datetime.now().strftime('%Y-%m-%d')
            date = datetime.now().strftime('%Y-%m-%d')
            genre = "Comedy"
            director = "Kevin ken"
            rating = round(random.uniform(1, 10), 2)
            description = "This is a movie."
            args = (movie_name, watched_on, date, genre, director, rating, description)
            self.cursor.execute(
                "INSERT OR IGNORE INTO movies (name, watched_on, date, genre, director, rating, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
                args)
        self.connection.commit()

    def populate_dummy_books_data(self):
        # Generate and insert dummy data for books
        for _ in range(10):  # Insert 10 dummy books
            game_name = f"Book {random.randint(1, 100)}"
            date = datetime.now().strftime('%Y-%m-%d')
            genre = "Action"
            author = "Dan Brown"
            rating = round(random.uniform(1, 10), 2)
            description = "This is a dummy book."
            args = (game_name, date, genre, author, rating, description)
            self.cursor.execute(
                "INSERT OR IGNORE INTO books (name, date, genre, author, rating, description) VALUES (?, ?, ?, ?, ?, ?)",
                args)
        self.connection.commit()

    def search_items(self, table_name, keyword):
        self.db_type = table_name

        # Get the column names of the table
        self.cursor.execute(f"PRAGMA table_info({self.db_type})")
        columns = [col[1] for col in self.cursor.fetchall()]

        # Generate the WHERE condition for each column
        where_conditions = [f"{col} LIKE ?" for col in columns]

        # Combine the conditions with OR
        where_clause = " OR ".join(where_conditions)

        # Create the parameters list for the placeholders
        params = ["%" + keyword + "%" for _ in columns]

        # Construct the full query
        query = f"SELECT * FROM {self.db_type} WHERE {where_clause}"
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return rows

    def add_game(self, game):
        insert_query = """
        INSERT INTO games (name, date, genre, company, rating, description)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        values = (game.name, game.date, game.genre, game.company, game.rating, game.description)
        self.cursor.execute(insert_query, values)
        self.connection.commit()

    def add_movie(self, movie):
        insert_query = """
        INSERT INTO movies (name, watched_on, date, genre, director, rating, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            movie.name, movie.watched_on, movie.date, movie.genre, movie.director, movie.rating, movie.description)
        self.cursor.execute(insert_query, values)
        self.connection.commit()

    def add_book(self, book):
        insert_query = """
           INSERT INTO books (name, date, genre, author, rating, description)
           VALUES (?, ?, ?, ?, ?, ?)
           """
        values = (book.name, book.date, book.genre, book.author, book.rating, book.description)
        self.cursor.execute(insert_query, values)
        self.connection.commit()

    def edit_game(self, game):
        update_query = """
        UPDATE games SET name=?, date=?, genre=?, company=?, rating=?, description=?
        WHERE id=?
        """
        values = (game.name, game.date, game.genre, game.company, game.rating, game.description, game.id)
        self.cursor.execute(update_query, values)
        self.connection.commit()

    def edit_movie(self, movie):
        update_query = """
        UPDATE movies SET name=?, watched_on=?, date=?, genre=?, director=?, rating=?, description=?
        WHERE id=?
        """
        values = (
            movie.name, movie.watched_on, movie.date, movie.genre, movie.director, movie.rating, movie.description,
            movie.id)
        self.cursor.execute(update_query, values)
        self.connection.commit()

    def edit_book(self, book):
        update_query = """
        UPDATE books SET name=?, date=?, genre=?, author=?, rating=?, description=?
        WHERE id=?
        """
        values = (book.name, book.date, book.genre, book.author, book.rating, book.description, book.id)
        self.cursor.execute(update_query, values)
        self.connection.commit()

    def delete_item(self, table_name, item_id):
        self.db_type = table_name
        delete_query = f"DELETE FROM {self.db_type} WHERE id = ?"
        self.cursor.execute(delete_query, (item_id,))
        self.connection.commit()


class Game:
    def __init__(self, name, date, genre, company, rating, description):
        self.name = name
        self.date = date
        self.genre = genre
        self.company = company
        self.rating = rating
        self.description = description


class Movie:
    def __init__(self, name, watched_on, date, genre, director, rating, description):
        self.name = name
        self.watched_on = watched_on
        self.date = date
        self.genre = genre
        self.director = director
        self.rating = rating
        self.description = description


class Book:
    def __init__(self, name, date, genre, author, rating, description):
        self.name = name
        self.date = date
        self.genre = genre
        self.author = author
        self.rating = rating
        self.description = description
