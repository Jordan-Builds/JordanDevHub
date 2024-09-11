import tkinter as tk
from tkinter import messagebox
import hashlib  # For password hashing

class MovieManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Movie Manager")

        # Database connection
        

        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.modify_movie_id_var = tk.StringVar()

        # Login Page
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)
        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, pady=5)
        tk.Entry(self.login_frame, textvariable=self.username_var).grid(row=0, column=1, pady=5)
        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, pady=5)
        tk.Entry(self.login_frame, textvariable=self.password_var, show="*").grid(row=1, column=1, pady=5)
        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.login_frame, text="Create User", command=self.open_create_user_window).grid(row=3, column=0, columnspan=2, pady=10)
        

        self.logged_in = False

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "SELECT * FROM users WHERE username = %s AND userPassword = %s"
        self.cursor.execute(query, (username, hashed_password))
        result = self.cursor.fetchone()
        if result:
            self.logged_in = True
            self.show_main_page()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def show_main_page(self):
        self.login_frame.destroy()

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # Arrange buttons in a single column
        tk.Button(self.main_frame, text="Add Movie", command=self.open_add_movie_window).grid(row=0, column=0, pady=5, padx=5)
        tk.Button(self.main_frame, text="Delete Movie", command=self.open_delete_movie_window).grid(row=1, column=0, pady=5, padx=5)
        tk.Button(self.main_frame, text="Modify Movie", command=self.open_modify_movie_window).grid(row=2, column=0, pady=5, padx=5)
        tk.Button(self.main_frame, text="Display Movies", command=self.display_movies).grid(row=3, column=0, pady=5, padx=5)
        tk.Button(self.main_frame, text="Search Movie", command=self.search_movie).grid(row=4, column=0, pady=5, padx=5)
        tk.Button(self.main_frame, text="Display Watched Movies", command=self.display_watched_movies).grid(row=5, column=0, pady=5, padx=5)
        tk.Button(self.main_frame, text="Display To Be Watched Movies", command=self.display_to_be_watched_movies).grid(row=6, column=0, pady=5, padx=5)

        # Logout button at the bottom
        tk.Button(self.main_frame, text="Logout", command=self.logout).grid(row=7, column=0, pady=10, padx=5)

    def open_add_movie_window(self):
        add_movie_window = tk.Toplevel(self.root)
        add_movie_window.title("Add Movie")

        tk.Label(add_movie_window, text="Movie ID:").grid(row=0, column=0, pady=5)
        movie_id_entry = tk.Entry(add_movie_window)
        movie_id_entry.grid(row=0, column=1, pady=5)

        tk.Label(add_movie_window, text="Director:").grid(row=1, column=0, pady=5)
        director_entry = tk.Entry(add_movie_window)
        director_entry.grid(row=1, column=1, pady=5)

        tk.Label(add_movie_window, text="Actor:").grid(row=2, column=0, pady=5)
        actor_entry = tk.Entry(add_movie_window)
        actor_entry.grid(row=2, column=1, pady=5)

        tk.Label(add_movie_window, text="Description:").grid(row=3, column=0, pady=5)
        description_entry = tk.Entry(add_movie_window)
        description_entry.grid(row=3, column=1, pady=5)

        movie_status_var = tk.StringVar()
        movie_status_var.set("Watchlist")
        tk.Label(add_movie_window, text="Movie Status:").grid(row=4, column=0, pady=5)
        tk.Radiobutton(add_movie_window, text="Watchlist", variable=movie_status_var, value="Watchlist").grid(row=4, column=1, pady=5)
        tk.Radiobutton(add_movie_window, text="Watched", variable=movie_status_var, value="Watched").grid(row=4, column=2, pady=5)

        tk.Button(add_movie_window, text="Add Movie", command=lambda: self.add_movie_details(
            movie_id_entry.get(), director_entry.get(), actor_entry.get(), description_entry.get(), movie_status_var.get())).grid(row=5, column=0, columnspan=3, pady=10)

    def add_movie_details(self, movie_id, director, actor, description, status):
        try:
            query = "INSERT INTO movie (movieID, director, actor, descript) VALUES (%s, %s, %s, %s)"
            self.cursor.execute(query, (movie_id, director, actor, description))
            if status == "Watchlist":
                self.cursor.execute("INSERT INTO toBeWatched (TBWmovieID) VALUES (%s)", (movie_id,))
            elif status == "Watched":
                self.cursor.execute("INSERT INTO watched (WmovieID) VALUES (%s)", (movie_id,))
            self.db_connection.commit()
            messagebox.showinfo("Movie Added", "Movie added successfully")
        except err as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def open_delete_movie_window(self):
        delete_movie_window = tk.Toplevel(self.root)
        delete_movie_window.title("Delete Movie")

        tk.Label(delete_movie_window, text="Movie ID:").grid(row=0, column=0, pady=5)
        movie_id_entry = tk.Entry(delete_movie_window)
        movie_id_entry.grid(row=0, column=1, pady=5)

        tk.Button(delete_movie_window, text="Delete Movie", command=lambda: self.delete_movie_details(
            movie_id_entry.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def delete_movie_details(self, movie_id):
        try:
            query = "DELETE FROM movie WHERE movieID = %s"
            self.cursor.execute(query, (movie_id,))
            self.db_connection.commit()
            messagebox.showinfo("Movie Deleted", f"Movie ID {movie_id} deleted successfully")
        except err as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def open_modify_movie_window(self):
        modify_movie_id_window = tk.Toplevel(self.root)
        modify_movie_id_window.title("Modify Movie - Enter Movie ID")

        tk.Label(modify_movie_id_window, text="Movie ID:").grid(row=0, column=0, pady=5)
        movie_id_entry = tk.Entry(modify_movie_id_window, textvariable=self.modify_movie_id_var)
        movie_id_entry.grid(row=0, column=1, pady=5)

        tk.Button(modify_movie_id_window, text="Next", command=lambda: self.open_modify_options_window(
            movie_id_entry.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def open_modify_options_window(self, movie_id):
        modify_options_window = tk.Toplevel(self.root)
        modify_options_window.title("Modify Movie - Choose Option")

        tk.Label(modify_options_window, text=f"Choose aspect to modify for Movie ID {movie_id}:").grid(row=0, column=0, columnspan=2, pady=5)

        tk.Button(modify_options_window, text="Modify Director", command=lambda: self.modify_movie_details(
            movie_id, "Director")).grid(row=1, column=0, pady=5)
        tk.Button(modify_options_window, text="Modify Actor", command=lambda: self.modify_movie_details(
            movie_id, "Actor")).grid(row=1, column=1, pady=5)
        tk.Button(modify_options_window, text="Modify Description", command=lambda: self.modify_movie_details(
            movie_id, "Description")).grid(row=2, column=0, columnspan=2, pady=5)

    def modify_movie_details(self, movie_id, modification_option):
        modify_details_window = tk.Toplevel(self.root)
        modify_details_window.title(f"Modify {modification_option} for Movie ID: {movie_id}")

        tk.Label(modify_details_window, text=f"Enter new {modification_option}:").grid(row=0, column=0, pady=5)
        new_value_entry = tk.Entry(modify_details_window)
        new_value_entry.grid(row=0, column=1, pady=5)

        tk.Button(modify_details_window, text="Update", command=lambda: self.update_movie_details(
            movie_id, modification_option, new_value_entry.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def update_movie_details(self, movie_id, modification_option, new_value):
        try:
            if modification_option in ["Director", "Actor", "Description"]:
                field = modification_option.lower()
                query = f"UPDATE movie SET {field} = %s WHERE movieID = %s"
                self.cursor.execute(query, (new_value, movie_id))
                self.db_connection.commit()
                messagebox.showinfo("Update Successful", f"{modification_option} for Movie ID {movie_id} updated to: {new_value}")
            else:
                messagebox.showerror("Error", "Invalid modification option")
        except err as err:
            messagebox.showerror("Error", f"An error occurred: {err}")
            
    def display_movies(self):
        display_window = tk.Toplevel(self.root)
        display_window.title("Movie List")

        try:
            self.cursor.execute("SELECT movieID, director, actor, descript FROM movie")
            rows = self.cursor.fetchall()
            
            # Creating a Listbox to display movies
            movie_listbox = tk.Listbox(display_window, width=100, height=10)
            movie_listbox.pack(padx=10, pady=10)

            # Populating the Listbox
            for row in rows:
                movie_listbox.insert(tk.END, f"ID: {row[0]}, Director: {row[1]}, Actor: {row[2]}, Description: {row[3]}")

            # Buttons to add movies to Watched or To Be Watched lists
            tk.Button(display_window, text="Add to Watched", command=lambda: self.add_to_watched(movie_listbox.get(tk.ANCHOR))).pack(padx=10, pady=5)
            tk.Button(display_window, text="Add to To Be Watched", command=lambda: self.add_to_to_be_watched(movie_listbox.get(tk.ANCHOR))).pack(padx=10, pady=5)
        except err as err:
            messagebox.showerror("Error", f"An error occurred: {err}") 
            
    def open_create_user_window(self):
        create_user_window = tk.Toplevel(self.root)
        create_user_window.title("Create User")

        tk.Label(create_user_window, text="Username:").grid(row=0, column=0, pady=5)
        username_entry = tk.Entry(create_user_window)
        username_entry.grid(row=0, column=1, pady=5)

        tk.Label(create_user_window, text="Password:").grid(row=1, column=0, pady=5)
        password_entry = tk.Entry(create_user_window, show="*")
        password_entry.grid(row=1, column=1, pady=5)

        tk.Label(create_user_window, text="Email:").grid(row=2, column=0, pady=5)
        email_entry = tk.Entry(create_user_window)
        email_entry.grid(row=2, column=1, pady=5)

        tk.Button(create_user_window, text="Create", command=lambda: self.create_user(
            username_entry.get(), password_entry.get(), email_entry.get())).grid(row=3, column=0, columnspan=2, pady=10)

    def create_user(self, username, password, email):
        # Create user method implementation...
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            query = "INSERT INTO users (username, userPassword, email) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (username, hashed_password, email))
            self.db_connection.commit()
            messagebox.showinfo("User Created", "New user created successfully")
        except err as err:
            messagebox.showerror("Error", f"An error occurred: {err}")
            
    def search_movie(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Movie")

        tk.Label(search_window, text="Enter Movie ID:").grid(row=0, column=0, pady=5)
        movie_id_entry = tk.Entry(search_window)
        movie_id_entry.grid(row=0, column=1, pady=5)

        tk.Button(search_window, text="Search", command=lambda: self.find_movie(movie_id_entry.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def find_movie(self, movie_id):
        try:
            query = "SELECT movieID, director, actor, descript FROM movie WHERE movieID = %s"
            self.cursor.execute(query, (movie_id,))
            movie = self.cursor.fetchone()
            if movie:
                movie_id, director, actor, description = movie
                messagebox.showinfo("Movie Found", f"ID: {movie_id}\nDirector: {director}\nActor: {actor}\nDescription: {description}")
            else:
                messagebox.showinfo("Movie Not Found", "No movie found with that ID")
        except err as err:
            messagebox.showerror("Error", f"An error occurred: {err}")
            
            
    def add_to_watched(self, movie_info):
        movie_id = self.extract_movie_id(movie_info)
        if movie_id:
            try:
                query = "INSERT INTO watched (WmovieID) VALUES (%s)"
                self.cursor.execute(query, (movie_id,))
                self.db_connection.commit()
                messagebox.showinfo("Success", f"Movie ID {movie_id} added to Watched list")
            except err as err:
                messagebox.showerror("Error", f"An error occurred: {err}")

    def add_to_to_be_watched(self, movie_info):
        movie_id = self.extract_movie_id(movie_info)
        if movie_id:
            try:
                query = "INSERT INTO toBeWatched (TBWmovieID) VALUES (%s)"
                self.cursor.execute(query, (movie_id,))
                self.db_connection.commit()
                messagebox.showinfo("Success", f"Movie ID {movie_id} added to To Be Watched list")
            except err as err:
                messagebox.showerror("Error", f"An error occurred: {err}")

    def extract_movie_id(self, movie_info):
        try:
            return movie_info.split(",")[0].split(":")[1].strip()
        except IndexError:
            messagebox.showerror("Error", "Invalid movie selection")
            return None
            
            
    def display_watched_movies(self):
        self.display_movies_list("watched")

    def display_to_be_watched_movies(self):
        self.display_movies_list("toBeWatched")

    def display_movies_list(self, list_type):
        display_window = tk.Toplevel(self.root)
        display_window.title(f"{list_type} Movies")

        try:
            if list_type == "watched":
                query = "SELECT movie.movieID, movie.director, movie.actor, movie.descript FROM movie INNER JOIN watched ON movie.movieID = watched.WmovieID"
            else:
                query = "SELECT movie.movieID, movie.director, movie.actor, movie.descript FROM movie INNER JOIN toBeWatched ON movie.movieID = toBeWatched.TBWmovieID"

            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            
            movie_listbox = tk.Listbox(display_window, width=100, height=10)
            movie_listbox.pack(padx=10, pady=10)

            for row in rows:
                movie_listbox.insert(tk.END, f"ID: {row[0]}, Director: {row[1]}, Actor: {row[2]}, Description: {row[3]}")
        except err as err:
            messagebox.showerror("Error", f"An error occurred: {err}")


    def logout(self):
        self.root.destroy()

    def run(self):
        # Run the application...
        self.root.mainloop()

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'db_connection') and self.db_connection:
            self.db_connection.close()

if __name__ == "__main__":
    app = MovieManager()
    app.run()