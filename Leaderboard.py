import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Leaderboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Leaderboard")
        self.root.geometry("600x350")

        self.create_database_table()

        self.frame = Frame(root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

        self.tree = ttk.Treeview(self.frame, column=("c0", "c1", "c2"), show='headings') # Create a treeview widget
        self.tree.column("#1", anchor=CENTER, width=150)
        self.tree.heading("#1", text="Position")
        self.tree.column("#2", anchor=CENTER, width=150)
        self.tree.heading("#2", text="User")
        self.tree.column("#3", anchor=CENTER, width=150)
        self.tree.heading("#3", text="Time")
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        button1 = Button(self.frame, text="Display data", command=self.display_data)
        button1.grid(row=1, column=0, pady=10)

    def create_database_table(self):
        conn = sqlite3.connect("rubixcubesolver.db")
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Leaderboard (
                username VARCHAR(20),
                time TEXT
            )
        """)
        conn.commit()
        conn.close()

    def display_data(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect("rubixcubesolver.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM Leaderboard ORDER BY time ASC")# Select all data from the Leaderboard table in ascending order of time
        rows = cur.fetchall()
        for index, row in enumerate(rows, start=1):
            self.tree.insert("", END, values=(index, row[0], row[1]))

        conn.close()

        # Calculate overall average time
        conn = sqlite3.connect("rubixcubesolver.db")
        cur = conn.cursor()
        cur.execute("SELECT AVG(CAST(SUBSTR(time, 1, 2) AS INTEGER) * 60 + CAST(SUBSTR(time, 4, 2) AS INTEGER)) FROM "
                    "Leaderboard")
        overall_average_seconds = cur.fetchone()[0]
        conn.close()

        # Convert overall average time to mm:ss format
        overall_average_minutes = overall_average_seconds // 60
        overall_average_seconds = overall_average_seconds % 60
        overall_average_time_string = f"{int(overall_average_minutes):02d}:{int(overall_average_seconds):02d}"

        # Display overall average time in a message box
        messagebox.showinfo("Overall Average Time", f"The overall average time is {overall_average_time_string}.")


def main():
    root = Tk()
    leaderboard_gui = Leaderboard(root)
    root.mainloop()


if __name__ == '__main__':
    main()

