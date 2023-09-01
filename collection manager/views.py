from tkinter import ttk
from tkinter import *

from models import Game, Movie, Book


class GUI:
    def __init__(self, root, collection_manager, db):
        self.root = root
        self.collection_manager = collection_manager
        self.db = db

        self.table_name = 'games'
        self.game_frame = None
        self.game_treeview = None
        self.movie_frame = None
        self.movie_treeview = None
        self.book_frame = None
        self.book_treeview = None

        self.root.title("Collection Manager")
        self.tab_control = ttk.Notebook(self.root)

        self.recent_all_labels = {
            "all": "All",
            "recent": "Recent",
        }

        self.game_tab = ttk.Frame(self.tab_control)
        self.movie_tab = ttk.Frame(self.tab_control)
        self.book_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.game_tab, text="Games")
        self.tab_control.add(self.movie_tab, text="Movies")
        self.tab_control.add(self.book_tab, text="Books")
        self.tab_control.pack(expand=1, fill="both")

        self.create_game_tab()
        self.create_movie_tab()
        self.create_book_tab()

        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        selected_tab_id = event.widget.select()
        selected_tab = event.widget.tab(selected_tab_id, "text")
        if selected_tab == 'Games':
            self.table_name = 'games'
        elif selected_tab == 'Movies':
            self.table_name = 'movies'
        elif selected_tab == 'Books':
            self.table_name = 'books'

    def create_game_tab(self):
        self.table_name = 'games'
        key = 'recent'
        self.game_frame = ttk.LabelFrame(self.game_tab, text=f"{self.recent_all_labels[key]} Games")
        self.game_frame.pack(fill="both", expand=True, padx=10, pady=10)
        # Using Treeview to display games as a table

        # Create a frame to hold Treeview and Scrollbar
        tree_frame = ttk.Frame(self.game_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("ID", "Name", "Date", "Genre", "Company", "Rating", "Description")
        self.game_treeview = ttk.Treeview(tree_frame, columns=columns, show="headings")

        for col in columns:
            self.game_treeview.heading(col, text=col, anchor="center")
            if col == 'ID':
                self.game_treeview.column(col, width=75, stretch=False, anchor="center")
            elif col == 'Description':
                self.game_treeview.column(col, width=500, stretch=True)
            else:
                self.game_treeview.column(col, width=200, stretch=True)
        self.game_treeview.pack(side="left", fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)  # Set height of the row

        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.game_treeview.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.game_treeview.configure(yscrollcommand=tree_scrollbar.set)

        # Buttons for CRUD operations
        add_button = ttk.Button(self.game_frame, text="Add Game", command=self.add_game)
        add_button.pack(side="top", padx=5, pady=5)

        edit_button = ttk.Button(self.game_frame, text="Edit Game", command=lambda: self.edit_game(self.game_treeview))
        edit_button.pack(side="top", padx=5, pady=5)

        delete_button = ttk.Button(self.game_frame, text="Delete Game",
                                   command=lambda: self.delete_item(self.game_treeview))
        delete_button.pack(side="top", padx=5, pady=5)

        all_button = ttk.Button(self.game_frame, text="Show all Games",
                                command=lambda: self.show_all_items(self.game_treeview, self.game_frame))
        all_button.pack(side="top", padx=5, pady=5)

        # Search box
        search_label = ttk.Label(self.game_frame, text="Search:")
        search_label.pack(side="top", padx=5, pady=5)

        search_entry = ttk.Entry(self.game_frame)
        search_entry.pack(side="top", padx=5, pady=5)

        search_button = ttk.Button(self.game_frame, text="Search",
                                   command=lambda: self.search_item(
                                       self.game_treeview,
                                       self.table_name,
                                       search_entry.get())
                                   )
        search_button.pack(side="top", padx=5, pady=5)

        self.load_games(self.game_treeview)

    def create_movie_tab(self):
        self.table_name = 'movies'
        key = 'recent'
        self.movie_frame = ttk.LabelFrame(self.movie_tab, text=f"{self.recent_all_labels[key]} Movie")
        self.movie_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree_frame = ttk.Frame(self.movie_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("ID", "Name", "Watched on", "Date", "Genre", "Director", "Rating", "Description")

        self.movie_treeview = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.movie_treeview.heading(col, text=col, anchor="center")
            if col == 'ID':
                self.movie_treeview.column(col, width=75, stretch=False, anchor="center")
            elif col == 'Description':
                self.movie_treeview.column(col, width=500, stretch=True)
            else:
                self.movie_treeview.column(col, width=200, stretch=True)
        self.movie_treeview.pack(side="left", fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.movie_treeview.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.movie_treeview.configure(yscrollcommand=tree_scrollbar.set)

        # Buttons for CRUD operations
        add_button = ttk.Button(self.movie_frame, text="Add Movie", command=self.add_movie)
        add_button.pack(side="top", padx=5, pady=5)

        edit_button = ttk.Button(self.movie_frame, text="Edit Movie",
                                 command=lambda: self.edit_movie(self.movie_treeview))
        edit_button.pack(side="top", padx=5, pady=5)

        delete_button = ttk.Button(self.movie_frame, text="Delete Movie",
                                   command=lambda: self.delete_item(self.movie_treeview))
        delete_button.pack(side="top", padx=5, pady=5)

        all_button = ttk.Button(self.movie_frame, text="Show all Movies",
                                command=lambda: self.show_all_items(self.movie_treeview, self.movie_frame))
        all_button.pack(side="top", padx=5, pady=5)

        # Search box
        search_label = ttk.Label(self.movie_frame, text="Search:")
        search_label.pack(side="top", padx=5, pady=5)

        search_entry = ttk.Entry(self.movie_frame)
        search_entry.pack(side="top", padx=5, pady=5)

        search_button = ttk.Button(self.movie_frame, text="Search",
                                   command=lambda: self.search_item(self.movie_treeview,
                                                                    self.table_name,
                                                                    search_entry.get())
                                   )
        search_button.pack(side="top", padx=5, pady=5)

        self.load_movies(self.movie_treeview)

    def create_book_tab(self):
        self.table_name = 'books'
        key = 'recent'
        self.book_frame = ttk.LabelFrame(self.book_tab, text=f"{self.recent_all_labels[key]} Books")
        self.book_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree_frame = ttk.Frame(self.book_frame)
        tree_frame.pack(fill="both", expand=True)

        columns = ("ID", "Name", "Date", "Genre", "Author", "Rating", "Description")

        self.book_treeview = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.book_treeview.heading(col, text=col, anchor="center")
            if col == 'ID':
                self.book_treeview.column(col, width=75, stretch=False, anchor="center")
            elif col == 'Description':
                self.book_treeview.column(col, width=500, stretch=True)
            else:
                self.book_treeview.column(col, width=200, stretch=True)
        self.book_treeview.pack(side="left", fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.book_treeview.yview)
        tree_scrollbar.pack(side="right", fill="y")
        self.book_treeview.configure(yscrollcommand=tree_scrollbar.set)

        # Buttons for CRUD operations
        add_button = ttk.Button(self.book_frame, text="Add Book", command=self.add_book)
        add_button.pack(side="top", padx=5, pady=5)

        edit_button = ttk.Button(self.book_frame, text="Edit Book", command=lambda: self.edit_book(self.book_treeview))
        edit_button.pack(side="top", padx=5, pady=5)

        delete_button = ttk.Button(self.book_frame, text="Delete Book",
                                   command=lambda: self.delete_item(self.book_treeview))
        delete_button.pack(side="top", padx=5, pady=5)

        all_button = ttk.Button(self.book_frame, text="Show all Books",
                                command=lambda: self.show_all_items(self.book_treeview, self.book_frame))
        all_button.pack(side="top", padx=5, pady=5)

        # Search box
        search_label = ttk.Label(self.book_frame, text="Search:")
        search_label.pack(side="top", padx=5, pady=5)

        search_entry = ttk.Entry(self.book_frame)
        search_entry.pack(side="top", padx=5, pady=5)

        search_button = ttk.Button(self.book_frame, text="Search",
                                   command=lambda: self.search_item(self.book_treeview,
                                                                    self.table_name,
                                                                    search_entry.get())
                                   )
        search_button.pack(side="top", padx=5, pady=5)

        self.load_books(self.book_treeview)

    def show_all_items(self, treeview, item_frame):
        results = self.collection_manager.search_items(self.table_name, '')
        treeview.delete(*treeview.get_children())

        for item in results:
            treeview.insert("", "end", values=item, tags=("row",))

        # Update label text
        new_label_text = f"{self.recent_all_labels['all']} {self.table_name.capitalize()}"
        item_frame.configure(text=new_label_text)

    def add_game(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Game")

        game_name_label = Label(add_window, text="Game Name:")
        game_name_label.grid(row=0, column=0, padx=10, pady=5)
        game_name_entry = Entry(add_window)
        game_name_entry.grid(row=0, column=1, padx=10, pady=5)

        game_data_label = Label(add_window, text="Release Date:")
        game_data_label.grid(row=1, column=0, padx=10, pady=5)
        game_data_entry = Entry(add_window)
        game_data_entry.grid(row=1, column=1, padx=10, pady=5)

        game_genre_label = Label(add_window, text="Genre:")
        game_genre_label.grid(row=2, column=0, padx=10, pady=5)
        game_genre_entry = Entry(add_window)
        game_genre_entry.grid(row=2, column=1, padx=10, pady=5)

        game_company_label = Label(add_window, text="Company:")
        game_company_label.grid(row=3, column=0, padx=10, pady=5)
        game_company_entry = Entry(add_window)
        game_company_entry.grid(row=3, column=1, padx=10, pady=5)

        game_rating_label = Label(add_window, text="Rating:")
        game_rating_label.grid(row=4, column=0, padx=10, pady=5)
        game_rating_entry = Entry(add_window)
        game_rating_entry.grid(row=4, column=1, padx=10, pady=5)

        game_description_label = Label(add_window, text="Description:")
        game_description_label.grid(row=5, column=0, padx=10, pady=5)
        game_description_entry = Entry(add_window)
        game_description_entry.grid(row=5, column=1, padx=10, pady=5)

        save_button = Button(add_window, text="Save",
                             command=lambda: self.save_game(add_window,
                                                            game_name_entry.get(),
                                                            game_data_entry.get(),
                                                            game_genre_entry.get(),
                                                            game_company_entry.get(),
                                                            game_rating_entry.get(),
                                                            game_description_entry.get()))
        save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def add_movie(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Movie")

        movie_name_label = Label(add_window, text="Movie Name:")
        movie_name_label.grid(row=0, column=0, padx=10, pady=5)
        movie_name_entry = Entry(add_window)
        movie_name_entry.grid(row=0, column=1, padx=10, pady=5)

        movie_watched_label = Label(add_window, text="Watched on:")
        movie_watched_label.grid(row=1, column=0, padx=10, pady=5)
        movie_watched_entry = Entry(add_window)
        movie_watched_entry.grid(row=1, column=1, padx=10, pady=5)

        movie_data_label = Label(add_window, text="Release Date:")
        movie_data_label.grid(row=2, column=0, padx=10, pady=5)
        movie_data_entry = Entry(add_window)
        movie_data_entry.grid(row=2, column=1, padx=10, pady=5)

        movie_genre_label = Label(add_window, text="Genre:")
        movie_genre_label.grid(row=3, column=0, padx=10, pady=5)
        movie_genre_entry = Entry(add_window)
        movie_genre_entry.grid(row=3, column=1, padx=10, pady=5)

        movie_director_label = Label(add_window, text="Director:")
        movie_director_label.grid(row=4, column=0, padx=10, pady=5)
        movie_director_entry = Entry(add_window)
        movie_director_entry.grid(row=4, column=1, padx=10, pady=5)

        movie_rating_label = Label(add_window, text="Rating:")
        movie_rating_label.grid(row=5, column=0, padx=10, pady=5)
        movie_rating_entry = Entry(add_window)
        movie_rating_entry.grid(row=5, column=1, padx=10, pady=5)

        movie_description_label = Label(add_window, text="Description:")
        movie_description_label.grid(row=6, column=0, padx=10, pady=5)
        movie_description_entry = Entry(add_window)
        movie_description_entry.grid(row=6, column=1, padx=10, pady=5)

        save_button = Button(add_window, text="Save",
                             command=lambda: self.save_movie(add_window, movie_name_entry.get(),
                                                             movie_watched_entry.get(),
                                                             movie_data_entry.get(),
                                                             movie_genre_entry.get(),
                                                             movie_director_entry.get(),
                                                             movie_rating_entry.get(),
                                                             movie_description_entry.get()
                                                             )
                             )
        save_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def add_book(self):
        add_window = Toplevel(self.root)
        add_window.title("Add Book")

        book_name_label = Label(add_window, text="Book Name:")
        book_name_label.grid(row=0, column=0, padx=10, pady=5)
        book_name_entry = Entry(add_window)
        book_name_entry.grid(row=0, column=1, padx=10, pady=5)

        book_data_label = Label(add_window, text="Release Date:")
        book_data_label.grid(row=1, column=0, padx=10, pady=5)
        book_data_entry = Entry(add_window)
        book_data_entry.grid(row=1, column=1, padx=10, pady=5)

        book_genre_label = Label(add_window, text="Genre:")
        book_genre_label.grid(row=2, column=0, padx=10, pady=5)
        book_genre_entry = Entry(add_window)
        book_genre_entry.grid(row=2, column=1, padx=10, pady=5)

        book_author_label = Label(add_window, text="Author:")
        book_author_label.grid(row=3, column=0, padx=10, pady=5)
        book_author_entry = Entry(add_window)
        book_author_entry.grid(row=3, column=1, padx=10, pady=5)

        book_rating_label = Label(add_window, text="Rating:")
        book_rating_label.grid(row=4, column=0, padx=10, pady=5)
        book_rating_entry = Entry(add_window)
        book_rating_entry.grid(row=4, column=1, padx=10, pady=5)

        book_description_label = Label(add_window, text="Description:")
        book_description_label.grid(row=5, column=0, padx=10, pady=5)
        book_description_entry = Entry(add_window)
        book_description_entry.grid(row=5, column=1, padx=10, pady=5)

        save_button = Button(add_window, text="Save",
                             command=lambda: self.save_book(add_window,
                                                            book_name_entry.get(),
                                                            book_data_entry.get(),
                                                            book_genre_entry.get(),
                                                            book_author_entry.get(),
                                                            book_rating_entry.get(),
                                                            book_description_entry.get()))
        save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def save_game(self, add_window, game_name, date, genre, company, rating, description):
        new_game = Game(game_name, date, genre, company, rating, description)

        self.collection_manager.add_game(new_game)
        self.load_games(self.game_treeview)
        add_window.destroy()

        new_label_text = f"{self.recent_all_labels['recent']} {self.table_name.capitalize()}"
        self.game_frame.configure(text=new_label_text)

    def save_movie(self, add_window, movie_name, watched, date, genre, director, rating, description):
        new_movie = Movie(movie_name, watched, date, genre, director, rating, description)

        self.collection_manager.add_movie(new_movie)
        self.load_movies(self.movie_treeview)
        add_window.destroy()

        new_label_text = f"{self.recent_all_labels['recent']} {self.table_name.capitalize()}"
        self.movie_frame.configure(text=new_label_text)

    def save_book(self, add_window, book_name, date, genre, author, rating, description):
        new_book = Book(book_name, date, genre, author, rating, description)

        self.collection_manager.add_book(new_book)
        self.load_books(self.book_treeview)
        add_window.destroy()

        new_label_text = f"{self.recent_all_labels['recent']} {self.table_name.capitalize()}"
        self.book_frame.configure(text=new_label_text)

    def edit_game(self, game_treeview):
        selected_item = game_treeview.selection()

        if selected_item:
            item_values = game_treeview.item(selected_item, "values")
            selected_game_id = item_values[0]
            selected_game = self.collection_manager.get_item_by_id(selected_game_id, self.table_name)

            add_window = Toplevel(self.root)
            add_window.title("Edit Game")

            game_name_label = Label(add_window, text="Game Name:")
            game_name_label.grid(row=0, column=0, padx=10, pady=5)
            game_name_entry = Entry(add_window)
            game_name_entry.grid(row=0, column=1, padx=10, pady=5)
            game_name_entry.insert(0, selected_game[1])

            game_data_label = Label(add_window, text="Release Date:")
            game_data_label.grid(row=1, column=0, padx=10, pady=5)
            game_data_entry = Entry(add_window)
            game_data_entry.grid(row=1, column=1, padx=10, pady=5)
            game_data_entry.insert(0, selected_game[2])

            game_genre_label = Label(add_window, text="Genre:")
            game_genre_label.grid(row=2, column=0, padx=10, pady=5)
            game_genre_entry = Entry(add_window)
            game_genre_entry.grid(row=2, column=1, padx=10, pady=5)
            game_genre_entry.insert(0, selected_game[3])

            game_company_label = Label(add_window, text="Company:")
            game_company_label.grid(row=3, column=0, padx=10, pady=5)
            game_company_entry = Entry(add_window)
            game_company_entry.grid(row=3, column=1, padx=10, pady=5)
            game_company_entry.insert(0, selected_game[4])

            game_rating_label = Label(add_window, text="Rating:")
            game_rating_label.grid(row=4, column=0, padx=10, pady=5)
            game_rating_entry = Entry(add_window)
            game_rating_entry.grid(row=4, column=1, padx=10, pady=5)
            game_rating_entry.insert(0, selected_game[5])

            game_description_label = Label(add_window, text="Description:")
            game_description_label.grid(row=5, column=0, padx=10, pady=5)
            game_description_entry = Entry(add_window)
            game_description_entry.grid(row=5, column=1, padx=10, pady=5)
            game_description_entry.insert(0, selected_game[6])

            save_button = Button(add_window, text="Save",
                                 command=lambda: self.save_edited_game(add_window, selected_game_id,
                                                                       game_name_entry.get(),
                                                                       game_data_entry.get(),
                                                                       game_genre_entry.get(),
                                                                       game_company_entry.get(),
                                                                       game_rating_entry.get(),
                                                                       game_description_entry.get()))
            save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def edit_movie(self, movie_treeview):
        selected_item = movie_treeview.selection()

        if selected_item:
            item_values = movie_treeview.item(selected_item, "values")
            selected_movie_id = item_values[0]
            selected_movie = self.collection_manager.get_item_by_id(selected_movie_id, self.table_name)

            add_window = Toplevel(self.root)
            add_window.title("Edit Movie")

            movie_name_label = Label(add_window, text="Movie Name:")
            movie_name_label.grid(row=0, column=0, padx=10, pady=5)
            movie_name_entry = Entry(add_window)
            movie_name_entry.grid(row=0, column=1, padx=10, pady=5)
            movie_name_entry.insert(0, selected_movie[1])

            movie_watched_label = Label(add_window, text="Watched on:")
            movie_watched_label.grid(row=1, column=0, padx=10, pady=5)
            movie_watched_entry = Entry(add_window)
            movie_watched_entry.grid(row=1, column=1, padx=10, pady=5)
            movie_watched_entry.insert(0, selected_movie[2])

            movie_data_label = Label(add_window, text="Release Date:")
            movie_data_label.grid(row=2, column=0, padx=10, pady=5)
            movie_data_entry = Entry(add_window)
            movie_data_entry.grid(row=2, column=1, padx=10, pady=5)
            movie_data_entry.insert(0, selected_movie[3])

            movie_genre_label = Label(add_window, text="Genre:")
            movie_genre_label.grid(row=3, column=0, padx=10, pady=5)
            movie_genre_entry = Entry(add_window)
            movie_genre_entry.grid(row=3, column=1, padx=10, pady=5)
            movie_genre_entry.insert(0, selected_movie[4])

            movie_director_label = Label(add_window, text="Director:")
            movie_director_label.grid(row=4, column=0, padx=10, pady=5)
            movie_director_entry = Entry(add_window)
            movie_director_entry.grid(row=4, column=1, padx=10, pady=5)
            movie_director_entry.insert(0, selected_movie[5])

            movie_rating_label = Label(add_window, text="Rating:")
            movie_rating_label.grid(row=5, column=0, padx=10, pady=5)
            movie_rating_entry = Entry(add_window)
            movie_rating_entry.grid(row=5, column=1, padx=10, pady=5)
            movie_rating_entry.insert(0, selected_movie[6])

            movie_description_label = Label(add_window, text="Description:")
            movie_description_label.grid(row=6, column=0, padx=10, pady=5)
            movie_description_entry = Entry(add_window)
            movie_description_entry.grid(row=6, column=1, padx=10, pady=5)
            movie_description_entry.insert(0, selected_movie[7])

            save_button = Button(add_window, text="Save",
                                 command=lambda: self.save_edited_movie(add_window, selected_movie_id,
                                                                        movie_name_entry.get(),
                                                                        movie_watched_entry.get(),
                                                                        movie_data_entry.get(),
                                                                        movie_genre_entry.get(),
                                                                        movie_director_entry.get(),
                                                                        movie_rating_entry.get(),
                                                                        movie_description_entry.get()))
            save_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def edit_book(self, book_treeview):
        selected_item = book_treeview.selection()

        if selected_item:
            item_values = book_treeview.item(selected_item, "values")
            selected_book_id = item_values[0]
            selected_book = self.collection_manager.get_item_by_id(selected_book_id, self.table_name)

            add_window = Toplevel(self.root)
            add_window.title("Edit Book")

            book_name_label = Label(add_window, text="Book Name:")
            book_name_label.grid(row=0, column=0, padx=10, pady=5)
            book_name_entry = Entry(add_window)
            book_name_entry.grid(row=0, column=1, padx=10, pady=5)
            book_name_entry.insert(0, selected_book[1])

            book_data_label = Label(add_window, text="Release Date:")
            book_data_label.grid(row=1, column=0, padx=10, pady=5)
            book_data_entry = Entry(add_window)
            book_data_entry.grid(row=1, column=1, padx=10, pady=5)
            book_data_entry.insert(0, selected_book[2])

            book_genre_label = Label(add_window, text="Genre:")
            book_genre_label.grid(row=2, column=0, padx=10, pady=5)
            book_genre_entry = Entry(add_window)
            book_genre_entry.grid(row=2, column=1, padx=10, pady=5)
            book_genre_entry.insert(0, selected_book[3])

            book_author_label = Label(add_window, text="Author:")
            book_author_label.grid(row=3, column=0, padx=10, pady=5)
            book_author_entry = Entry(add_window)
            book_author_entry.grid(row=3, column=1, padx=10, pady=5)
            book_author_entry.insert(0, selected_book[4])

            book_rating_label = Label(add_window, text="Rating:")
            book_rating_label.grid(row=4, column=0, padx=10, pady=5)
            book_rating_entry = Entry(add_window)
            book_rating_entry.grid(row=4, column=1, padx=10, pady=5)
            book_rating_entry.insert(0, selected_book[5])

            book_description_label = Label(add_window, text="Description:")
            book_description_label.grid(row=5, column=0, padx=10, pady=5)
            book_description_entry = Entry(add_window)
            book_description_entry.grid(row=5, column=1, padx=10, pady=5)
            book_description_entry.insert(0, selected_book[6])

            save_button = Button(add_window, text="Save",
                                 command=lambda: self.save_edited_book(add_window, selected_book_id,
                                                                       book_name_entry.get(),
                                                                       book_data_entry.get(),
                                                                       book_genre_entry.get(),
                                                                       book_author_entry.get(),
                                                                       book_rating_entry.get(),
                                                                       book_description_entry.get()))
            save_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def save_edited_game(self, edit_window, game_id, game_name, date, genre, company, rating, description):
        edited_game = Game(game_name, date, genre, company, rating, description)
        edited_game.id = game_id
        self.collection_manager.edit_game(edited_game)
        self.load_games(self.game_treeview)
        edit_window.destroy()
        new_label_text = f"{self.recent_all_labels['recent']} {self.table_name.capitalize()}"
        self.game_frame.configure(text=new_label_text)

    def save_edited_book(self, edit_window, book_id, book_name, date, genre, author, rating, description):
        edited_book = Book(book_name, date, genre, author, rating, description)
        edited_book.id = book_id
        self.collection_manager.edit_book(edited_book)
        self.load_books(self.book_treeview)
        edit_window.destroy()
        new_label_text = f"{self.recent_all_labels['recent']} {self.table_name.capitalize()}"
        self.book_frame.configure(text=new_label_text)

    def save_edited_movie(self, edit_window, movie_id, movie_name, watched, date, genre, director, rating, description):
        edited_movie = Movie(movie_name, watched, date, genre, director, rating, description)
        edited_movie.id = movie_id
        self.collection_manager.edit_movie(edited_movie)
        self.load_movies(self.movie_treeview)
        edit_window.destroy()
        new_label_text = f"{self.recent_all_labels['recent']} {self.table_name.capitalize()}"
        self.movie_frame.configure(text=new_label_text)

    def delete_item(self, item_treeview):
        selected_item = item_treeview.selection()
        if selected_item:
            item_values = item_treeview.item(selected_item, "values")
            selected_item_id = item_values[0]
            self.collection_manager.delete_item(self.table_name, selected_item_id)
            if self.table_name == 'games':
                self.load_games(item_treeview)
                new_label_text = f"{self.recent_all_labels['recent']} {self.table_name.capitalize()}"
                self.game_frame.configure(text=new_label_text)
            elif self.table_name == 'movies':
                self.load_movies(item_treeview)
                new_label_text = f"{self.recent_all_labels['recent']} {self.table_name.capitalize()}"
                self.movie_frame.configure(text=new_label_text)
            elif self.table_name == 'books':
                self.load_books(item_treeview)

    def search_item(self, item_treeview, table, keyword):
        self.table_name = table
        results = self.collection_manager.search_items(self.table_name, keyword)
        item_treeview.delete(*item_treeview.get_children())
        for item in results:
            item_treeview.insert("", "end", values=item, tags=("row",))

    def load_games(self, treeview):
        treeview.delete(*treeview.get_children())
        games = self.collection_manager.games[-5:]
        for game in reversed(games):
            self.game_treeview.insert("", "end", values=game, tags=("row",))

    def load_movies(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)
        movies = self.collection_manager.movies[-5:]
        for movie in reversed(movies):
            self.movie_treeview.insert("", "end", values=movie, tags=("row",))

    def load_books(self, treeview):
        treeview.delete(*treeview.get_children())
        books = self.collection_manager.books[-5:]
        for book in reversed(books):
            self.book_treeview.insert("", "end", values=book, tags=("row",))

    def run(self):
        self.root.mainloop()
