import os
import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
from queue import Queue

class StelleAI:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Stelle AI - Chat")
        self.root.geometry("400x500")

        # Create a header frame for the profile name and image
        self.header_frame = tk.Frame(self.root, bg="#000080")
        self.header_frame.pack(fill="x", pady=0)

        # Load the profile image
        self.load_profile_image()

        # Add a label for the profile name with specified font
        self.profile_name = tk.Label(self.header_frame, text="Stelle", fg="white", bg="#000080", font=("Helvetica Neue", 12))
        self.profile_name.pack(side="left", padx=10)

        # Create a frame for displaying messages
        self.chat_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.chat_frame.pack(fill="both", expand=True)

        # Create a text widget for displaying messages
        self.chat_text = tk.Text(self.chat_frame, width=40, height=10, font=("Roboto", 10), bg="#FFFFFF")
        self.chat_text.pack(fill="both", expand=True)

        # Create a frame for inputting messages
        self.input_frame = tk.Frame(self.root, bg="#000080", pady=10)
        self.input_frame.pack(fill="x", pady=0)

        # Create an entry for inputting messages
        self.input_entry = tk.Entry(self.input_frame, width=45, font=("Roboto", 10))
        self.input_entry.pack(side="left", fill="x", expand=True, padx=10)

        # Create a button for sending messages
        self.send_button = tk.Button(self.input_frame, text="Kirim", command=self.send_message, bg="#000080", fg="#FFFFFF")
        self.send_button.pack(side="right", fill="y", expand=False, padx=10)

        # Create a queue for storing messages
        self.message_queue = Queue()

        # Bind Enter key to send message
        self.input_entry.bind("<Return>", self.send_message)

    def load_profile_image(self):
        try:
            current_dir = os.path.abspath(os.path.dirname(__file__))
            image_path = os.path.join(current_dir, "photo.jpg")
            image = Image.open(image_path)
            image = image.resize((50, 50), resample=Image.LANCZOS)
            self.profile_image = ImageTk.PhotoImage(image)
            self.profile_image_label = tk.Label(self.header_frame, image=self.profile_image, bg="#000080")
            self.profile_image_label.pack(side="left", padx=10)
        except Exception as e:
            print("Gagal memuat foto profile:", e)
            self.profile_image_label = tk.Label(self.header_frame, text="No Image", bg="#000080", fg="white")
            self.profile_image_label.pack(side="left", padx=10)

    def send_message(self, event=None):
        message = self.input_entry.get()
        if message:
            self.message_queue.put(f"Anda: {message}")
            self.input_entry.delete(0, "end")
            self.respond_to_message(message)

    def respond_to_message(self, message):
        try:
            conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "DB", "Training.db"))
            c = conn.cursor()
            c.execute("SELECT response FROM training_data WHERE prompt=?", (message,))
            response = c.fetchone()
            if response:
                self.message_queue.put(f"Stelle: {response[0]}")
            else:
                self.message_queue.put("Stelle: Maaf, saya tidak mengerti.")
            conn.close()
            self.display_message()
        except Exception as e:
            print("Error accessing the database:", e)
            self.message_queue.put("Stelle: Terjadi kesalahan saat mengakses database.")
            self.display_message()

    def display_message(self):
        while not self.message_queue.empty():
            message = self.message_queue.get()
            self.chat_text.insert("end", message + "\n")
            self.chat_text.see("end")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = StelleAI(root, "username")
    app.run()