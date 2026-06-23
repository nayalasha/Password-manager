import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import random
import string

# ---------------- DATABASE ----------------

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT,
    username TEXT,
    password TEXT
)
""")

conn.commit()

# ---------------- APPEARANCE ----------------

ctk.set_appearance_mode("dark")

# ---------------- WINDOW ----------------

window = ctk.CTk()
window.title("Password Manager")
window.geometry("1280x720")
window.resizable(False, False)

# ---------------- PASSWORD GENERATOR ----------------

def generate_password():
    characters = (
        string.ascii_letters +
        string.digits +
        "!@#$%^&*"
    )

    generated_password = ""

    for i in range(12):
        generated_password += random.choice(characters)

    return generated_password

# ---------------- FUNCTIONS ----------------

def submit():
    website_info = website.get()
    username_info = username.get()
    password_info = password.get()

    if website_info == "" or username_info == "" or password_info == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    cursor.execute(
        "INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
        (website_info, username_info, password_info)
    )

    conn.commit()

    update_textbox()

    messagebox.showinfo(
        "Success",
        "Password saved successfully!"
    )

    website.delete(0, "end")
    username.delete(0, "end")
    password.delete(0, "end")


def update_textbox():
    listbox.configure(state="normal")
    listbox.delete("1.0", "end")

    cursor.execute(
        "SELECT website, username, password FROM passwords"
    )

    rows = cursor.fetchall()

    for row in rows:
        listbox.insert(
            "end",
            f"Website: {row[0]}\n"
            f"Username: {row[1]}\n"
            f"Password: {row[2]}\n\n"
        )

    listbox.configure(state="disabled")


def make_password():
    password.delete(0, "end")
    password.insert(0, generate_password())


def toggle_password_visibility():
    if password.cget("show") == "*":
        password.configure(show="")
    else:
        password.configure(show="*")


def search():
    website_name = website.get()

    cursor.execute(
        "SELECT username, password FROM passwords WHERE LOWER(website)=LOWER(?)",
        (website_name,)
    )

    result = cursor.fetchone()

    if result:
        messagebox.showinfo(
            "Website Found",
            f"Username: {result[0]}\nPassword: {result[1]}"
        )
    else:
        messagebox.showwarning(
            "Not Found",
            "No password saved for that website."
        )


def delete():
    website_name = website.get()

    cursor.execute(
        "SELECT * FROM passwords WHERE LOWER(website)=LOWER(?)",
        (website_name,)
    )

    result = cursor.fetchone()

    if result:
        cursor.execute(
            "DELETE FROM passwords WHERE LOWER(website)=LOWER(?)",
            (website_name,)
        )

        conn.commit()

        update_textbox()

        messagebox.showinfo(
            "Success",
            "Password deleted."
        )
    else:
        messagebox.showwarning(
            "Not Found",
            "Website not found."
        )

    website.delete(0, "end")

# ---------------- TITLE ----------------

title = ctk.CTkLabel(
    window,
    text="Password Manager",
    font=("Arial", 30, "bold")
)
title.pack(pady=20)

# ---------------- FRAMES ----------------

left_frame = ctk.CTkFrame(window)
left_frame.pack(side="left", padx=50, pady=20)

right_frame = ctk.CTkFrame(window)
right_frame.pack(side="right", padx=50, pady=20)

# ---------------- ENTRIES ----------------

website = ctk.CTkEntry(
    left_frame,
    width=300,
    placeholder_text="Website"
)
website.pack(pady=10)

username = ctk.CTkEntry(
    left_frame,
    width=300,
    placeholder_text="Username"
)
username.pack(pady=10)

password = ctk.CTkEntry(
    left_frame,
    width=300,
    placeholder_text="Password",
    show="*"
)
password.pack(pady=10)

# ---------------- CHECKBOX ----------------

show_password = ctk.CTkCheckBox(
    left_frame,
    text="Show Password",
    command=toggle_password_visibility
)
show_password.pack(pady=10)

# ---------------- BUTTONS ----------------

generate_button = ctk.CTkButton(
    left_frame,
    text="Generate Password",
    command=make_password
)
generate_button.pack(pady=10)

submit_button = ctk.CTkButton(
    left_frame,
    text="Save Password",
    command=submit
)
submit_button.pack(pady=10)

search_button = ctk.CTkButton(
    left_frame,
    text="Search",
    command=search
)
search_button.pack(pady=10)

delete_title = ctk.CTkLabel(
    left_frame,
    text="Enter a website name above to delete it.",
    font=("Arial", 10)
)
delete_title.pack(pady=(15, 5))

delete_button = ctk.CTkButton(
    left_frame,
    text="Delete",
    command=delete
)
delete_button.pack(pady=10)

# ---------------- RIGHT SIDE ----------------

saved_label = ctk.CTkLabel(
    right_frame,
    text="Saved Passwords",
    font=("Arial", 20, "bold")
)
saved_label.pack(pady=10)

listbox = ctk.CTkTextbox(
    right_frame,
    width=500,
    height=400,
    state="disabled",
    font=("Arial", 12)
)
listbox.pack(pady=10)

# ---------------- START ----------------

update_textbox()

window.mainloop()