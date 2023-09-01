from tkinter import *
from models import DB
from views import GUI


class CollectionManager:
    def __init__(self, database):
        self.db = database
        self.movies = []
        self.games = []
        self.books = []
        self.table_name = 'games'

    def load_data(self):
        if self.table_name == 'games':
            self.games = self.db.get_items(self.table_name)
        elif self.table_name == 'movies':
            self.movies = self.db.get_items(self.table_name)
        elif self.table_name == 'books':
            self.books = self.db.get_items(self.table_name)

    def load_movie_data(self):
        # Load data from DB only first time when create movie tab
        self.movies = self.db.get_items('movies')

    def load_book_data(self):
        # Load data from DB only first time when create book tab
        self.books = self.db.get_items('books')

    def add_game(self, game):
        self.db.add_game(game)
        self.table_name = 'games'
        self.load_data()

    def add_movie(self, movie):
        self.db.add_movie(movie)
        self.table_name = 'movies'
        self.load_data()

    def add_book(self, book):
        self.db.add_book(book)
        self.table_name = 'books'
        self.load_data()

    def edit_game(self, game):
        self.db.edit_game(game)
        self.table_name = 'games'
        self.load_data()

    def edit_book(self, book):
        self.db.edit_book(book)
        self.table_name = 'books'
        self.load_data()

    def edit_movie(self, movie):
        self.db.edit_movie(movie)
        self.table_name = 'movies'
        self.load_data()

    def get_item_by_id(self, item_id, table):
        if table == 'games':
            for item in self.games:
                if item[0] == int(item_id):
                    return item
        elif table == 'movies':
            for item in self.movies:
                if item[0] == int(item_id):
                    return item
        elif table == 'books':
            for item in self.books:
                if item[0] == int(item_id):
                    return item

    def search_items(self, table, keyword):
        table_name = table
        result_list = self.db.search_items(table_name, keyword)
        return result_list

    def delete_item(self, table, item_id):
        self.table_name = table
        self.db.delete_item(table, item_id)
        self.load_data()

    def __del__(self):
        self.db.connection.close()


if __name__ == "__main__":
    root = Tk()
    db = DB()
    # db.populate_dummy_games_data()
    # db.populate_dummy_movies_data()
    # db.populate_dummy_books_data()
    collection_manager = CollectionManager(db)
    collection_manager.load_data()
    collection_manager.load_movie_data()
    collection_manager.load_book_data()
    gui = GUI(root, collection_manager, db)
    gui.run()
