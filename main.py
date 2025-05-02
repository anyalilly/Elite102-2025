import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt # to hash the passwords and protect them

db = mysql.connector.connect( # Connecting to MYSQL database
    host="localhost", 
    user="root",
    password="Anya54559",
    database="bank_app"

)

cursor = db.cursor() # to send commands to the database

# Signing a user up
def sign_up():
    print()
    print("Sign Up:")
    print()
    username = entry_username.get()
    password = entry_password.get()
    full_name = entry_fullname.get()
    pin = entry_pin.get()

    if not (username and password and pin and full_name):
         messagebox.showerror("Error", "Please fill in all fields.")
         return

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
         cursor.execute("INSERT INTO users (username, password, full_name, pin) VALUES (%s, %s, %s, %s)", (username, hashed_pw.decode('utf-8'), full_name, pin))
         db.commit()
         cursor.execute("SELECT user_id FROM user WHERE username = %s", (username,))
         result = cursor.fetchone()
         if result:
              user_id = result[0]
         cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (%s, %s)", (user_id, 0.0))
         db.commit()

         messagebox.showinfo("Success", "Your account has been created!")
    except mysql.connector.Error as err:
         messagebox.showerror("Error", str(err))
                             

def login():
     print("")
     print("Log In!")
     username = entry_username.get()
     password = entry_password.get()

     cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
     result = cursor.fetchone()

     if result:
          user_id = result[0]
          stored_hashed_pw = result[1]
          if result:
               user_id, stored_pw = result
               if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_pw.encode('utf-8')):
                    show_dshboard(user_id)
               else:
                    messagebox.showerror("Error", "Your username was not found in the database.")

def show_dshboard(user_id):
     dashboard = tk.Toplevel()
     dashboard.title("Bank Dashboard")

     def check_balance():
          cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
          result = cursor.fetchone()[0]
          if result:
               balance = result[0]
               messagebox.showinfo("Balance", f"Your balance is: ${balance:.2f}")
     def deposit():
          amount = simple_entry_popup("Deposit", "Enter amount to deposit: ")
          if amount:
               cursor.execute("UPDATE accounts SET balance = balance + %s WHERE user_id = %s", (amount, user_id))
               db.commit()
               messagebox.showinfo("Success", "Your deposit has been completed!")
     def withdraw():
          amount = simple_entry_popup("Withdraw", "Enter amount to withdraw: ")
          if amount:
               cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
               balance = cursor.fetchone()[0]
               if result is not None:
                    balance = result[0]
               else:
                    balance = 0
               if balance >= amount:
                    cursor.execute("UPDATE accounts SET balance = balance - %s WHERE user_id = %s", (amount, user_id))
                    db.commit()
                    messagebox.showinfo("Success", "Your withdrawal has been completed!")
               else:
                    messagebox.showerror("Error", "Insufficient funds")

     def update_info():
        new_name = simple_entry_popup("Update Name", "Enter new full name:")
        new_pin = simple_entry_popup("Update PIN", "Enter new PIN:")
        if new_name:
            cursor.execute("UPDATE users SET full_name = %s WHERE user_id = %s", (new_name, user_id))
        if new_pin:
            cursor.execute("UPDATE users SET pin = %s WHERE user_id = %s", (new_pin, user_id))
        db.commit()
        messagebox.showinfo("Updated", "Your info has been updated!")

     def simple_entry_popup(title, prompt, validator=None):
        popup = tk.Toplevel()
        popup.title(title)

        tk.Label(popup, text=prompt).pack()
        entry = tk.Entry(popup)
        entry.pack()

        result = tk.StringVar()

        def submit():
            value = entry.get().strip()
            if validator and not validator(value):
                 messagebox.showinfo("Error", "Invalid input")
                 return result.set(value)
                 popup.destory()
            tk.Button(popup, text="Submit", command=submit).pack()
        popup.grab_set()
        popup.wait_window(popup)
        return result.get() if result.get() else None

        submit_btn = tk.Button(popup, text="Submit", command=submit)
        submit_btn.pack()

        popup.grab_set()
        app.wait_window(popup)

        return result.get() if result.get() else None

     btn_balance = tk.Button(dashboard, text="Check Balance", command=check_balance)
     btn_balance.pack(pady=5)

     btn_deposit = tk.Button(dashboard, text="Deposit", command=deposit)
     btn_deposit.pack(pady=5)

     btn_withdraw = tk.Button(dashboard, text="Withdraw", command=withdraw)
     btn_withdraw.pack(pady=5)

     btn_update = tk.Button(dashboard, text="Edit Info", command=update_info)
     btn_update.pack(pady=5)
def login():
     print("")
     print("Log In!")
     username = entry_username.get()
     password = entry_password.get()

     cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
     result = cursor.fetchone()

     if result:
          user_id = result[0]
          stored_hashed_pw = result[1]
          if result:
               user_id, stored_pw = result
               if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_pw.encode('utf-8')):
                    show_dshboard(user_id)
               else:
                    messagebox.showerror("Error", "Your username was not found in the database.")
# GUI Setup
app = tk.Tk()
app.title("Simple Bank App")

label_username = tk.Label(app, text="Username")
label_username.pack()
entry_username = tk.Entry(app)
entry_username.pack()

label_password = tk.Label(app, text="Password")
label_password.pack()
entry_password = tk.Entry(app, show="*")
entry_password.pack()

label_fullname = tk.Label(app, text="Full Name (For Sign Up)")
label_fullname.pack()
entry_fullname = tk.Entry(app)
entry_fullname.pack()

label_pin = tk.Label(app, text="PIN (For Sign Up)")
label_pin.pack()
entry_pin = tk.Entry(app, show="*")
entry_pin.pack()

button_signup = tk.Button(app, text="Sign Up", command=sign_up)
button_signup.pack()

button_login = tk.Button(app, text="Log In", command=login)
button_login.pack()

app.mainloop()


