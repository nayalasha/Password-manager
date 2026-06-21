import customtkinter as ctk
from tkinter import messagebox


# Appearance
ctk.set_appearance_mode("dark")

# Window
window = ctk.CTk()
window.title("Password Manager")
window.geometry("1280x720")
window.resizable(False, False)


# ---------- FUNCTIONS ----------

def submit():
    website_info = website.get()
    username_info = username.get()
    password_info = password.get()

    # Don't save empty entries
    if website_info == "" or username_info == "" or password_info == "":
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    # Save information
    with open("database.db", "a") as f:
        f.write(f"Website: {website_info}\n")
        f.write(f"Username: {username_info}\n")
        f.write(f"Password: {password_info}\n\n")

    # Update textbox
    update_textbox()

    # Popup
    messagebox.showinfo(
        "Success",
        "Password saved successfully!"
    )

    # Clear entries
    website.delete(0, "end")
    username.delete(0, "end")
    password.delete(0, "end")


def update_textbox():
    listbox.configure(state="normal")

    listbox.delete("1.0", "end")

    try:
        with open("database.db", "r") as f:
            contents = f.read()
            listbox.insert("1.0", contents)

    except FileNotFoundError:
        pass

    listbox.configure(state="disabled")


def make_password():
    password.delete(0, "end")
    password.insert(0, generate_password())


# ---------- TITLE ----------

title = ctk.CTkLabel(
    window,
    text="Password Manager",
    font=("Arial", 30, "bold")
)
title.pack(pady=20)


# ---------- ENTRIES ----------

website = ctk.CTkEntry(
    window,
    width=300,
    placeholder_text="Website"
)
website.pack(pady=10)

username = ctk.CTkEntry(
    window,
    width=300,
    placeholder_text="Username"
)
username.pack(pady=10)

password = ctk.CTkEntry(
    window,
    width=300,
    placeholder_text="Password",
    show="*"
)
password.pack(pady=10)


# ---------- BUTTONS ----------

generate_button = ctk.CTkButton(
    window,
    text="Generate Password",
    command=make_password
)
generate_button.pack(pady=10)

submit_button = ctk.CTkButton(
    window,
    text="Save Password",
    command=submit
)
submit_button.pack(pady=10)


# ---------- TEXTBOX ----------

listbox = ctk.CTkTextbox(
    window,
    width=500,
    height=250,
    state="disabled",
    font=("Arial", 12)
)
listbox.pack(pady=20)

# Generate password function
import random
import string

def generate_password():
    characters = string.ascii_letters + string.digits
    password = ""

    for i in range(12):
        password += random.choice(characters)

    return password




# Load saved passwords when the app starts
update_textbox()

# Run app
window.mainloop()