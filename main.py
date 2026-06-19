import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")

window = ctk.CTk()

# WIndow Settings
window.title("Password Manager")
window.geometry("1280x720")
window.resizable(False, False)

#def
def submit():
    website_info = website.get()
    username_info = username.get()
    password_info = password.get()

    website.delete(0, "end")
    username.delete(0, "end")
    password.delete(0, "end")

    with open("database.db", "a") as f:
        f.write(f"Website: {website_info}\n")
        f.write(f"Username: {username_info}\n")
        f.write(f"Password: {password_info}\n\n")
        update_textbox()
        messagebox.showinfo(
    "Success",
    "Password saved successfully!"
)

 

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
#Labels

title = ctk.CTkLabel(window, text="Password Manager",
                      font=("Arial", 24))
title.pack(pady=20)

website = ctk.CTkEntry(window, placeholder_text="Website")
website.pack(pady=10)

username = ctk.CTkEntry(window, placeholder_text="Username")
username.pack(pady=10)

password = ctk.CTkEntry(
    window,
    placeholder_text="Password",
    show="*"
)
password.pack(pady=10)

#Buttons
submit_button = ctk.CTkButton(
    window,
    text="Submit",
    command=submit
)
submit_button.pack(pady=10)

#listbox

listbox = ctk.CTkTextbox(window, width=400, height=200,
                          state="disabled",
                          font=("Arial", 12))
listbox.pack(pady=20)



update_textbox()
window.mainloop()