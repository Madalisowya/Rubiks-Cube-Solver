from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import solver
import Leaderboard
import sqlite3

# Connect to the SQLite database or create one if not exists
conn = sqlite3.connect("rubixcubesolver.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS Account (
        username VARCHAR(20) PRIMARY KEY,
        password VARCHAR(20)
    )
""")
conn.commit()


# Base class for common methods and attributes
class Base:
    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        pass

    def destroy_window(self):
        self.master.destroy()

    def check_username_exists(self, username):
        try:
            # Check if the username already exists in the database
            look = c.execute("""SELECT username FROM Account""")
            look = c.fetchall()

            for i in look:
                if username in i:
                    return True

            return False
        except:
            messagebox.showerror("This username doesnt exist")
            return False


# Login class for handling the login window, inheriting from Base
class Login(Base):
    def create_widgets(self):
        try:
            # GUI elements for login window
            self.username_label = ttk.Label(self.master, text="Username:")
            self.username_label.grid(row=0, column=0)
            self.username_entry = ttk.Entry(self.master, width=20)
            self.username_entry.grid(row=1, column=0, columnspan=2)

            self.password_label = ttk.Label(self.master, text="Password:")
            self.password_label.grid(row=2, column=0)
            self.password_entry = ttk.Entry(self.master, width=20, show="*")
            self.password_entry.grid(row=3, column=0, columnspan=2)

            self.submit_button = ttk.Button(self.master, text="Submit", command=self.getlogin)
            self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def getlogin(self):
        flag = False
        try:
            # Retrieve and validate login credentials
            username = self.username_entry.get()
            password = self.password_entry.get()

            if username == "" or password == "":
                messagebox.showerror("Error", "Please enter a username and a password.")
            else:
                look = c.execute("""SELECT username FROM Account""")
                look = c.fetchall()

                for i in look:
                    if username in i:
                        flag = True
                        break

                if flag:
                    look2 = c.execute("""SELECT password from Account WHERE username = (?)""", (username,))
                    actual_password = look2.fetchone()

                    if password == actual_password[0]:
                        messagebox.showinfo("Success", "Logged in!")
                        self.open_solver(username)
                        print(username)
                    else:
                        messagebox.showerror("Error", "Incorrect username or password.")
                else:
                    messagebox.showerror("Error", "Incorrect username or password.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def open_solver(self, username):
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.username_entry.focus_set()
        self.destroy_window()
        # Open Rubiks Cube Solver window
        root = Toplevel()
        root.title("Rubiks Cube Solver")
        root.resizable(False, False)
        app = solver.RubiksCubeSolver(root, username)
        app.init_gui()


# Register class for handling the registration window, inheriting from Base
class Register(Base):

    def create_widgets(self):
        try:
            # GUI elements for registration window
            self.username_label = ttk.Label(self.master, text="Username:")
            self.username_label.grid(row=0, column=0)
            self.username_entry = ttk.Entry(self.master, width=20)
            self.username_entry.grid(row=1, column=0, columnspan=2)

            self.password_label = ttk.Label(self.master, text="Password:")
            self.password_label.grid(row=2, column=0)
            self.password_entry = ttk.Entry(self.master, width=20, show="*")
            self.password_entry.grid(row=3, column=0, columnspan=2)

            self.submit_button = ttk.Button(self.master, text="Submit", command=self.regi)
            self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)
        except:
            messagebox.showerror("Error", "please enter a valid username or password")

    def regi(self):
        try:
            # Register a new user with provided credentials
            username = self.username_entry.get()
            password = self.password_entry.get()

            if username == "" or password == "":
                messagebox.showerror("Error", "Please enter a username and a password.")
            elif len(username) > 20:
                messagebox.showerror("Error", "Username must be less than 20 characters")

            else:
                if not self.check_username_exists(username):
                    c.execute("""INSERT INTO Account VALUES(?,?)""", (username, password))
                    conn.commit()
                    messagebox.showinfo("Success", "Registration successful!")
                    self.destroy_window()
                else:
                    messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        except:
            messagebox.showerror("Error", "please enter a valid username")


# Mainwindow class for the main application window, inheriting from Base
class Mainwindow(Base):
    def __init__(self, root_one):
        root_one.title("Mainwindow")
        # GUI elements for the main window
        self.logo = PhotoImage(file="rubiks.gif")
        ttk.Label(root_one, image=self.logo).grid(row=0, column=0, rowspan=2)
        self.button1 = ttk.Button(text="Log in", command=self.open_login_window)
        self.button1.grid(row=2, column=0, columnspan=2)

        self.button2 = ttk.Button(text="Register", command=self.open_Register_window)
        self.button2.grid(row=3, column=0, columnspan=2)

        self.button3 = ttk.Button(text="Leaderboard", command=self.open_Leaderboard_window)
        self.button3.grid(row=4, column=0, columnspan=2)

    def open_login_window(self):
        # Open login window
        login_window = Toplevel()
        login_window.title("Login")
        login_window.geometry("200x150")
        login_window.resizable(False, False)
        login = Login(login_window)

    def open_Register_window(self):
        # Open registration window
        register_window = Toplevel()
        register_window.title("Registration")
        register_window.geometry("200x150")
        register_window.resizable(False, False)
        register = Register(register_window)

    def open_Leaderboard_window(self):
        # Open leaderboard window
        Leaderboard_window = Toplevel()
        Leaderboard_window.title("Leaderboard")
        Leaderboard_window.resizable(False, False)
        Leader = Leaderboard.Leaderboard(Leaderboard_window)


def main():
    # Main function to start the application
    root = Tk()
    app = Mainwindow(root)
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()

conn.close()
