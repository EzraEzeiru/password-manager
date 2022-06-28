from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# .........................  PASSWORD GENERATOR ......................................#
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for char in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, string=f"{password}")
    pyperclip.copy(password)


# .........................  SAVE PASSWORD ...........................................#
def save_password():
    website = website_entry.get()
    email_or_username = email_or_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email_or_username,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any empty fields")
    else:
        is_okay = messagebox.askokcancel(title=website,
                                         message=f"These are the details entered:\nEmail: {email_or_username}\nPassword: {password}\nIs it okay to save?")

        if is_okay:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, "end")
                email_or_username_entry.delete(0, "end")
                password_entry.delete(0, "end")
                website_entry.focus()


def search_data():
    website = website_entry.get()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="You haven't typed in any data")
    else:
        try:
            with open("data.json") as data_file:
                data = json.load(data_file)
                website_name = data[website]["email"]
                website_password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email or Username: {website_name}\nPassword: {website_password}")

        except:
            messagebox.showinfo(title="Oops", message="This data does not exist")


# .........................  UI SETUP.............................................#
window = Tk()
window.title("Password Manger")
window.config(padx=50, pady=50)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1)

email_or_username_label = Label(text="Email/Username:")
email_or_username_label.grid(column=0, row=2)

email_or_username_entry = Entry(width=39)
email_or_username_entry.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, columnspan=2)

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=13, command=search_data)
search_button.grid(column=2, row=1)

canvas = Canvas(width=200, height=200)
padlock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 98, image=padlock_img)
canvas.grid(column=1, row=0)

window.mainloop()
