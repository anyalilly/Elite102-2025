import tkinter as tk # the GUI library
from tkinter import messagebox # for the popup messages
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
    # getting input values from the entry fields using Tkinter Entry widgets
    username = entry_username.get() 
    password = entry_password.get()
    full_name = entry_fullname.get()
    pin = entry_pin.get()
    # checks if any of the fields are empty
    if not (username and password and pin and full_name):
         messagebox.showerror("Error", "Please fill in all fields.")
         return
    
    # using bcrypt to hash the passwords and store them safely
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
         # inserting the user into the users table
         cursor.execute("INSERT INTO users (username, password, full_name, pin) VALUES (%s, %s, %s, %s)", (username, hashed_pw.decode('utf-8'), full_name, pin))
         db.commit() # to save the changes to the database
         cursor.execute("SELECT user_id FROM user WHERE username = %s", (username,))
         result = cursor.fetchone() # retrieves first matching row from the query
         if result:
              user_id = result[0] # gets the user id if there is a matching user
              # creates a bank account
              cursor.execute("INSERT INTO accounts (user_id, balance) VALUES (%s, %s)", (user_id, 0.0))
              db.commit()

              messagebox.showinfo("Success", "Your account has been created!")
         else:
          messagebox.showerror("Error", "Could not retrieve user ID after sign up.")
    except mysql.connector.Error as err: # catches errors from the database
         messagebox.showerror("Error", str(err))
                             

def login():
     print("")
     print("Log In!")
     username = entry_username.get()
     password = entry_password.get()
     # to check if there's matching existing user
     cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
     result = cursor.fetchone()

     if result:
          user_id, stored_pw = result
          if result:
               user_id, stored_pw = result
               # using bcrypt to verify the password
               if bcrypt.checkpw(password.encode('utf-8'), stored_pw.encode('utf-8')):
                    show_dshboard(user_id) # if the login goes through, it leads the user to the dashboard
               else:
                    messagebox.showerror("Error", "Your username was not found in the database.")

def show_dshboard(user_id):
     dashboard = tk.Toplevel() # to open a new window
     dashboard.title("Bank Dashboard")

     def check_balance():
          cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
          balance = cursor.fetchone()[0]
          messagebox.showinfo("Balance", f"Your balance is: ${balance:.2f}")
     def deposit():
        amount = simple_numeric_popup("Deposit", "Enter amount to deposit:")
        if amount:
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE user_id = %s", (amount, user_id))
            db.commit()
            messagebox.showinfo("Success", "Deposit completed!")
     def withdraw():
        amount = simple_numeric_popup("Withdraw", "Enter amount to withdraw:")
        if amount:
            cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
            balance = cursor.fetchone()[0]
            if balance >= amount:
                cursor.execute("UPDATE accounts SET balance = balance - %s WHERE user_id = %s", (amount, user_id))
                db.commit()
                messagebox.showinfo("Success", "Withdrawal completed!")
            else:
                messagebox.showerror("Error", "Insufficient funds")

     def update_info():
        new_name = simple_text_popup("Update Name", "Enter new full name:")
        new_pin = simple_text_popup("Update PIN", "Enter new PIN:")
        if new_name:
            cursor.execute("UPDATE users SET full_name = %s WHERE user_id = %s", (new_name, user_id))
        if new_pin:
            cursor.execute("UPDATE users SET pin = %s WHERE user_id = %s", (new_pin, user_id))
        db.commit()
        messagebox.showinfo("Updated", "Your info has been updated!")

     def simple_numeric_popup(title, prompt):
        popup = tk.Toplevel()
        popup.title(title)

        label = tk.Label(popup, text=prompt)
        label.pack()
        entry = tk.Entry(popup)
        entry.pack()

        result = tk.StringVar()

        def submit():
            try:
                val = float(entry.get())
                result.set(str(val))
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")

        submit_btn = tk.Button(popup, text="Submit", command=submit)
        submit_btn.pack()

        popup.grab_set()
        app.wait_window(popup)

        return float(result.get()) if result.get() else None

    # Popup for text inputs (like name or PIN)
     def simple_text_popup(title, prompt):
        popup = tk.Toplevel()
        popup.title(title)

        label = tk.Label(popup, text=prompt)
        label.pack()
        entry = tk.Entry(popup)
        entry.pack()

        result = tk.StringVar()

        def submit():
            result.set(entry.get())
            popup.destroy()

        submit_btn = tk.Button(popup, text="Submit", command=submit)
        submit_btn.pack()

        popup.grab_set()
        app.wait_window(popup)

        return result.get() if result.get() else None
# The dashboard's buttons
     tk.Button(dashboard, text="Check Balance", command=check_balance).pack(pady=5)
     tk.Button(dashboard, text="Deposit", command=deposit).pack(pady=5)
     tk.Button(dashboard, text="Withdraw", command=withdraw).pack(pady=5)
     tk.Button(dashboard, text="Edit Info", command=update_info).pack(pady=5)


# GUI Setup
app = tk.Tk() # the root window
app.title("Simple Bank App")
# Username
label_username = tk.Label(app, text="Username")
label_username.pack()
entry_username = tk.Entry(app)
entry_username.pack()
# For password
label_password = tk.Label(app, text="Password")
label_password.pack()
entry_password = tk.Entry(app, show="*")
entry_password.pack()
# For full name
label_fullname = tk.Label(app, text="Full Name (For Sign Up)")
label_fullname.pack()
entry_fullname = tk.Entry(app)
entry_fullname.pack()
# For pin
label_pin = tk.Label(app, text="PIN (For Sign Up)")
label_pin.pack()
entry_pin = tk.Entry(app, show="*")
entry_pin.pack()
# The sign up button
button_signup = tk.Button(app, text="Sign Up", command=sign_up)
button_signup.pack()
# The login button
button_login = tk.Button(app, text="Log In", command=login)
button_login.pack()

app.mainloop() # starts the app


