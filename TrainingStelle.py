import tkinter as tk
import sqlite3
import os

class TrainingStelle:
    def __init__(self, root):
        self.root = root
        self.root.title("Stelle AI - Training")
        self.root.geometry("400x500")

        # Create a frame for inputting prompts and answers
        self.input_frame = tk.Frame(self.root, bg="#F0F0F0")
        self.input_frame.pack(fill="both", expand=True)

        # Create a sub-frame to center the input elements
        self.center_frame = tk.Frame(self.input_frame, bg="#F0F0F0")
        self.center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create labels and entries for prompt and answer using grid
        self.prompt_label = tk.Label(self.center_frame, text="Prompt:", font=("Roboto", 10), anchor="w")
        self.prompt_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.prompt_entry = tk.Entry(self.center_frame, width=40, font=("Roboto", 10))
        self.prompt_entry.grid(row=1, column=0, padx=10, pady=5)

        self.answer_label = tk.Label(self.center_frame, text="Jawaban:", font=("Roboto", 10), anchor="w")
        self.answer_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.answer_entry = tk.Entry(self.center_frame, width=40, font=("Roboto", 10))
        self.answer_entry.grid(row=3, column=0, padx=10, pady=5)

        # Create a button to save the training data
        self.save_button = tk.Button(self.center_frame, text="Simpan", command=self.save_training_data, bg="#000080", fg="#FFFFFF")
        self.save_button.grid(row=4, column=0, padx=10, pady=10)

        self.feedback_label = tk.Label(self.center_frame, text="", font=("Roboto", 10), fg="green")
        self.feedback_label.grid(row=5, column=0, padx=10, pady=10)

        # Ensure the database and table are set up
        self.setup_database()

    def setup_database(self):
        try:
            conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "DB", "Training.db"))
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS training_data (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         prompt TEXT NOT NULL,
                         response TEXT NOT NULL)''')
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error setting up the database:", e)
            self.feedback_label.config(text="Terjadi kesalahan saat mengatur database.", fg="red")

    def save_training_data(self):
        prompt = self.prompt_entry.get()
        answer = self.answer_entry.get()
        if prompt and answer:
            try:
                conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), "DB", "Training.db"))
                c = conn.cursor()
                c.execute("INSERT INTO training_data (prompt, response) VALUES (?, ?)", (prompt, answer))
                conn.commit()
                conn.close()
                self.feedback_label.config(text="Data berhasil disimpan!", fg="green")
                self.prompt_entry.delete(0, "end")
                self.answer_entry.delete(0, "end")
            except Exception as e:
                print("Error saving to the database:", e)
                self.feedback_label.config(text="Terjadi kesalahan saat menyimpan data.", fg="red")
        else:
            self.feedback_label.config(text="Prompt dan jawaban tidak boleh kosong.", fg="red")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingStelle(root)
    app.run()