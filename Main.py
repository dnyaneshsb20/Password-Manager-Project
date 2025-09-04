from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project
def generate_password():
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
	           'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

	password_length = randint(8, 16)

	num_letters = randint(4, password_length - 4)
	num_symbols = randint(1, 3)
	num_numbers = password_length - num_letters - num_symbols

	password_letters = [choice(letters) for _ in range(num_letters)]
	password_symbols = [choice(symbols) for _ in range(num_symbols)]
	password_numbers = [choice(numbers) for _ in range(num_numbers)]

	password_list = password_letters + password_symbols + password_numbers
	shuffle(password_list)

	password = "".join(password_list)

	password_input.delete(0, END)  # Clear previous password
	password_input.insert(0, password)
	pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

	website = website_input.get()
	email = email_input.get()
	password = password_input.get()
	new_data = {
		website: {
			"Email":email,
			"Password":password,
		}
	}

	if len(website) == 0 or len(password) == 0:
		messagebox.showinfo(title="Oops!", message="Please make sure you haven't left any fields empty.")
	else:
		try:
			with open("Data.json","r") as data_file:
				data = json.load(data_file)
		except FileNotFoundError:
			with open("data.json", "w") as data_file:
				json.dump(new_data, data_file, indent=4)
		else:
			data.update(new_data)
			with open("Data.json","w") as data_file:
				json.dump(data, data_file,indent=4)
		finally:
			website_input.delete(0, END)
			password_input.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    user_input = website_input.get().strip()
    user_input_lower = user_input.lower()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        for stored_key in data:
            if stored_key.lower() == user_input_lower:
                email = data[stored_key]["Email"]
                password = data[stored_key]["Password"]
                messagebox.showinfo(
                    title=stored_key,
                    message=f"Email: {email}\nPassword: {password}"
                )
                return
        messagebox.showinfo(
            title="Error",
            message=f"No details exist for '{user_input}'."
        )
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50)

canvas = Canvas(width=200,height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(row=0,column=1)

website = Label(text="Website :")
website.grid(row=1,column=0)
website_input = Entry(width=32)
website_input.grid(row=1,column=1)
website_input.focus()

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(row=1,column=2)

email = Label(text="Email/Username :")
email.grid(row=2,column=0)
email_input = Entry(width=51)
email_input.grid(row=2,column=1,columnspan=2)
email_input.insert(0, "abc@gmail.com")

password = Label(text="Password :")
password.grid(row=3,column=0)
password_input = Entry(width=32)
password_input.grid(row=3,column=1)

generate_password = Button(text="Generate Password", command=generate_password)
generate_password.grid(row=3,column=2)

add_button = Button(text="Add",width=44,command=save)
add_button.grid(row=4,column=1,columnspan=2)
window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"+{x}+{y}")

window.mainloop()