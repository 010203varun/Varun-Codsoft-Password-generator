import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

# Initialize the database
with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
    db.commit()

class PasswordGeneratorApp:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.password_len = IntVar()
        self.generated_password = StringVar()

        self.setup_ui()

    def setup_ui(self):
        self.master.title('Password Generator')
        self.master.geometry('660x500')
        self.master.config(bg='#FF8000')
        self.master.resizable(False, False)

        Label(text=":PASSWORD GENERATOR:", anchor=N, fg='darkblue', bg='#FF8000', font='arial 20 bold underline').grid(row=0, column=1)
        
        Label(text="").grid(row=1, column=0, columnspan=2)
        
        Label(text="Enter User Name: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=2, column=0)
        Entry(textvariable=self.username, font='times 15', bd=6, relief='ridge').grid(row=2, column=1)
        
        Label(text="").grid(row=3, column=0, columnspan=2)
        
        Label(text="Enter Password Length: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=4, column=0)
        Entry(textvariable=self.password_len, font='times 15', bd=6, relief='ridge').grid(row=4, column=1)

        Label(text="").grid(row=5, column=0, columnspan=2)

        Label(text="Generated Password: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=6, column=0)
        Entry(textvariable=self.generated_password, font='times 15', bd=6, relief='ridge', fg='#DC143C').grid(row=6, column=1)

        Label(text="").grid(row=7, column=0, columnspan=2)

        Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='#68228B', bg='#BCEE68', command=self.generate_password).grid(row=8, column=1)

        Label(text="").grid(row=9, column=0, columnspan=2)

        Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.accept_password).grid(row=10, column=1)

        Label(text="").grid(row=11, column=0, columnspan=2)

        Button(text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.reset_fields).grid(row=12, column=1)

    def generate_password(self):
        upper = list(string.ascii_uppercase)
        lower = list(string.ascii_lowercase)
        chars = list("@#%&()\"?!")
        numbers = list(string.digits)
        name = self.username.get()
        length = self.password_len.get()

        if not name:
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be a string")
            self.username.set("")
            return

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        self.generated_password.set("")

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        generated_password = "".join(password)
        self.generated_password.set(generated_password)

    def accept_password(self):
        name = self.username.get()
        password = self.generated_password.get()

        if not name or not password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE Username = ?", (name,))
            if cursor.fetchone():
                messagebox.showerror("Error", "This username already exists! Please use another username.")
            else:
                cursor.execute("INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)", (name, password))
                db.commit()
                messagebox.showinfo("Success", "Password generated successfully")

    def reset_fields(self):
        self.username.set("")
        self.password_len.set(0)
        self.generated_password.set("")

if __name__ == '__main__':
    root = Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
