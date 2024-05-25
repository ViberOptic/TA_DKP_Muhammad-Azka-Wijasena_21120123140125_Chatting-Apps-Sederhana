import os
import sqlite3
import hashlib
import tkinter as tk
from tkinter import messagebox
from Chat import StelleAI
from TrainingStelle import TrainingStelle

def create_database():
    # Create a DB folder if it doesn't exist
    db_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "DB"))

    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    # Create a database connection and table in the DB folder
    db_file = os.path.join(db_folder, "User Data.db")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    return conn, cursor

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def query_user_data(cursor, username, password=None):
    if password:
        hashed_password = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    else:
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    return cursor.fetchone()

def check_user_data(user_data):
    return user_data is not None

def show_error_message(message):
    messagebox.showerror("Error", message)

def show_success_message(message):
    messagebox.showinfo("Berhasil", message)

def create_chat_window(username):
    root = tk.Tk()
    app = StelleAI(root, username)
    app.run()

class UserLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Stelle AI - Login")
        self.root.geometry("400x500")

        # Create a main frame for centering the content
        self.main_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.main_frame.pack(expand=True, fill="both")

        # Create a sub-frame for login form
        self.login_frame = tk.Frame(self.main_frame, bg="#F0F0F0")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create a label for username
        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Roboto", 10), bg="#F0F0F0")
        self.username_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        # Create an entry for inputting username
        self.username_entry = tk.Entry(self.login_frame, width=40, font=("Roboto", 10))
        self.username_entry.grid(row=1, column=0, padx=10, pady=(0, 10))

        # Create a label for password
        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Roboto", 10), bg="#F0F0F0")
        self.password_label.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))

        # Create an entry for inputting password
        self.password_entry = tk.Entry(self.login_frame, width=40, font=("Roboto", 10), show="*")
        self.password_entry.grid(row=3, column=0, padx=10, pady=(0, 10))

         # Create a frame for buttons
        self.button_frame = tk.Frame(self.login_frame, bg="#F0F0F0")
        self.button_frame.grid(row=4, column=0, pady=20)

        # Create a button for logging in
        self.login_button = tk.Button(self.button_frame, text="Masuk", command=self.login, font=("Roboto", 10), bg="#000080", fg="#FFFFFF")
        self.login_button.grid(row=0, column=0, padx=(0, 10))

        # Create a button for registering
        self.register_button = tk.Button(self.button_frame, text="Daftar", command=self.register, font=("Roboto", 10), bg="#000080", fg="#FFFFFF")
        self.register_button.grid(row=0, column=1)

        # Create a button for training AI
        self.train_button = tk.Button(self.button_frame, text="Training AI", command=self.train_ai, font=("Roboto", 10), bg="#000080", fg="#FFFFFF")
        self.train_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        # Create a database connection
        self.conn, self.cursor = create_database()

    def train_ai(self):
        # Open the training window
        TrainingStelle(tk.Toplevel())

    def login(self):
        # Get the inputted username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not password:
            show_error_message("Masukkan Password Terlebih Dahulu")
            return

        # Query the database for the user data
        user_data = query_user_data(self.cursor, username, password)

        # Check if the user data exists
        if check_user_data(user_data):
            # Close the login window
            self.root.destroy()

            # Open the chat window
            create_chat_window(username)
        else:
            # Show an error message
            show_error_message("Username atau password salah.")

    def register(self):
        # Get the inputted username and password
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not password:
            show_error_message("Masukkan Password Terlebih Dahulu")
            return

        # Hash the password
        hashed_password = hash_password(password)

        # Query the database for existing user
        existing_user = query_user_data(self.cursor, username)

        # Check if the user already exists
        if check_user_data(existing_user):
            # Show an error message
            show_error_message("Username telah digunakan.")
        else:
            # Insert the new user into the database
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            self.conn.commit()

            # Show a success message
            show_success_message("Pendaftaran berhasil, Silahkan Masuk.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = UserLogin(root)
    app.run()