from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import moves
import cube
import kociemba
import random
import Thyme
import sqlite3


# Defining the RubiksCubeSolver class
class RubiksCubeSolver():
    def __init__(self, root, username):
        # Initialize instance variables
        self.root = root
        self.cols = ["green", "blue", "white", "yellow", "red", "orange"]
        self.Cols = ["g", "b", "w", "y", "r", "o"]
        self.selected = 0
        self.faces = {
            self.cols[0]: cube.face[cube.green],
            self.cols[1]: cube.face[cube.blue],
            self.cols[2]: cube.face[cube.white],
            self.cols[3]: cube.face[cube.yellow],
            self.cols[4]: cube.face[cube.red],
            self.cols[5]: cube.face[cube.orange],
        }
        self.moves_list = ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'", "R2", "L2", "U2", "D2",
                           "F2", "B2"]
        self.selected_color_index = 0
        self.username = username  # Store the username as an instance variable
        self.solved = "R L U2 R L' B2 U2 R2 F2 L2 D2 L2 F2"

        self.timer = Thyme.Timer() # Create a Timer instance

# initialize the GUI
    def init_gui(self):
        self.init_frames()
        self.init_display_cube()
        self.init_mode_selector()
        self.init_colour_selector()
        self.init_options()
        self.init_output()
        self.init_cube_holder()
        self.init_cubies()
        self.init_moves_frame()
        self.init_timer()
        self.root.mainloop()

    # Initialise different frames in the GUI
    def init_frames(self):
        # Title frame
        self.title_frame = LabelFrame(self.root, padx=300, text="RUBIK CUBE SOLVER")
        # Frame to display the current state of the cube
        self.dispcube_frame = LabelFrame(self.root, padx=10, pady=15, text="Current State Of Cube")
        # Frame for selecting the solving mode
        self.mode_select_frame = LabelFrame(self.root, padx=60, pady=10, text="Select Mode")
        # Frame for selecting a color
        self.colour_sel_frame = LabelFrame(self.root, padx=35, pady=10, text="Pick A Colour")
        # Frame for performing cube moves
        self.preform_Move_frame = LabelFrame(self.root, padx=35, pady=10, text="Move the cube")

        # Other frames
        self.options_frame = LabelFrame(self.root, text="Options", padx=80, pady=10)
        self.output_frame = LabelFrame(self.root, padx=2, pady=2)
        self.timer_frame = LabelFrame(self.root, padx=31, pady=10)

    # Initialise the frame to display the current state of the cube
    def init_display_cube(self):
        self.dispcube_frame.grid(row=1, column=0, rowspan=4, padx=10)

    # Initialize the frame for selecting the solving mode
    def init_mode_selector(self):
        self.mode_var = IntVar()
        ttk.Radiobutton(self.mode_select_frame, text="Challenge! Solve cube yourself", variable=self.mode_var, value=1,
                        command=lambda: self.toggle_mode(enable_color_selectors=False, enable_timer_buttons=True)).pack(
            anchor=W)

        ttk.Radiobutton(self.mode_select_frame, text="Edit Side", variable=self.mode_var, value=0,
                        command=lambda: self.toggle_mode(enable_color_selectors=True, enable_timer_buttons=False)).pack(
            anchor=W)

        self.mode_select_frame.grid(row=1, column=1, padx=10)

    # Method to toggle between challenge mode and edit mode
    def toggle_mode(self, enable_color_selectors=True, enable_timer_buttons=True):
        # Enable/disable color selectors
        for selector in self.selectors:
            selector.config(state="normal" if enable_color_selectors else "disabled")

        for opt in self.options_frame.winfo_children():
            opt.config(state="normal" if enable_color_selectors else "disabled")

        # Enable/disable timer buttons
        for child in self.timer_frame.winfo_children():
            child.config(state="enabled" if enable_timer_buttons else "disabled")

        # stop timer if user toggles back to edit mode
        if not enable_timer_buttons:
            self.timer.stop_timer()
            self.reset_cube()

    # Initialise the frame for selecting a colour
    def init_colour_selector(self):
        # List to store colour selection buttons
        self.selectors = [
            Button(self.colour_sel_frame, width=6, height=2, highlightbackground=self.cols[i],
                   command=lambda i=i: self.select_and_edit_colour(i))
            for i in range(6)
        ]

        # Placing color selection buttons in a 2x3 grid
        for i, button in enumerate(self.selectors):
            button.grid(row=i // 3, column=i % 3, padx=5, pady=2)

        # Place the color selection frame in the main frame
        self.colour_sel_frame.grid(row=2, column=1, padx=10, pady=5)

    # Initialise the options frame
    def init_options(self):
        ttk.Button(self.options_frame, width=10, text="RESET CUBE", command=self.reset_cube).grid(row=0, column=0)
        ttk.Button(self.options_frame, width=17, text="GENERATE SOLUTION", command=self.generate_solution).grid(row=1,
                                                                                                                column=0)
        self.options_frame.grid(row=4, column=1, padx=10)

    def timer_frame(self):
        self.timer_frame.grid(row=5, column=1, padx=10)
        # initialise timer frame

    def init_timer(self):
        self.opt_entry.delete(0, END)

        ttk.Button(self.timer_frame, width=14, text="SOLVED!", state="disabled", command=self.timer_solution).grid(
            row=0, column=0)
        ttk.Button(self.timer_frame, width=14, text="▶", state="disabled",
                   command=lambda: (self.scramble_cube(), self.timer.start_timer())).grid(row=0, column=1)
        self.timer_frame.grid(row=5, column=1, padx=10)

    # Initialize the output frame
    def init_output(self):
        self.opt_entry = Entry(self.output_frame, width=70)
        self.opt_entry.grid(row=0, column=0)
        self.output_frame.grid(row=5, column=0, padx=10, pady=10)

    # Initialize the frame to hold the cube display
    def init_cube_holder(self):
        self.holder_frame = LabelFrame(self.dispcube_frame, highlightbackground="black")
        self.holder_frame.grid(row=1, column=1, rowspan=3, columnspan=3)

    # Initialize the cubies on the cube display
    def init_cubies(self):
        self.cubies = [
            Button(self.holder_frame, width=6, height=3)
            for i in range(9)
        ]
        self.show_cube_face()

    def moving(self, selected_color_index):
        # Set the selected color for editing
        self.selected = selected_color_index
        self.show_cube_face()

    # Handle color selection and initiate individual cubie editing
    def select_and_edit_colour(self, colour_index):
        # Update the currently selected selector
        self.selected = colour_index
        for i, button in enumerate(self.selectors):
            if i == colour_index:
                button.config(text="~", relief="sunken")
            else:
                button.config(text="", relief="raised")
        for i in self.cubies:
            i.config(state="normal", command=self.edit_cubie)

    def edit_cubie(self):
        # Enable editing mode for individual cubies
        # configure the state of the cubies to normal except the middle one (cubies[4])
        for button in self.cubies[0:4] + self.cubies[5:]:
            button.config(state="normal", command=lambda b=button: self.edit_cubie_color(b))

    # Edit the color of a cubie individually
    def edit_cubie_color(self, button):
        current = self.cubies[4].cget("highlightbackground")
        self.faces.get(current)
        # Update the face dictionary with the new color for the corresponding cubie
        self.faces[current][int(button.grid_info()['row'])][int(button.grid_info()['column'])] = self.Cols[
            self.selected]
        # Update the button's highlight background to reflect the new color
        button.config(highlightbackground=self.cols[self.selected])
        # Disable the button after editing
        button.config(state="disabled", command=lambda: self.edit_cubie_color(button))

    # Display the current state of the cube face
    def show_cube_face(self):
        n = 0
        curr = self.cols[self.selected]

        # Determine surrounding faces based on the selected face
        surrounding_faces = {
            "green": "2435",
            "blue": "2534",
            "white": "1405",
            "yellow": "0415",
            "red": "2130",
            "orange": "2031",
        }.get(curr)

        self.faces.get(curr) # Get the current face

        # Place the cubies on the cube display
        for i, button in enumerate(self.cubies):#all 9 cubies
            colour = {
                "g": self.cols[0],
                "b": self.cols[1],
                "w": self.cols[2],
                "y": self.cols[3],
                "r": self.cols[4],
                "o": self.cols[5],
            }.get(self.faces[curr][int(n / 3)][int(n % 3)])#get the color of the cubie based on the current face and the cubie index
            button.config(highlightbackground=colour, state="disabled") # Set the button's color and disable it
            button.grid(row=int(i // 3), column=int(n % 3), padx=2, pady=2)
            n += 1 # Increment the cubie index

        # Place the surrounding faces' centers
        Button(self.dispcube_frame, width=6, height=3, highlightbackground=self.cols[int(surrounding_faces[0])],
               state="normal",
               command=lambda: self.moving(int(surrounding_faces[0]))).grid(row=0, column=2,
                                                                            pady=40)  # top
        Button(self.dispcube_frame, width=6, height=3, highlightbackground=self.cols[int(surrounding_faces[1])],
               state="normal",
               command=lambda: self.moving(int(surrounding_faces[1]))).grid(row=2, column=4,
                                                                            padx=40)  # right
        Button(self.dispcube_frame, width=6, height=3, highlightbackground=self.cols[int(surrounding_faces[2])],
               state="normal",
               command=lambda: self.moving(int(surrounding_faces[2]))).grid(row=4, column=2,
                                                                            pady=40)  # bottom
        Button(self.dispcube_frame, width=6, height=3, highlightbackground=self.cols[int(surrounding_faces[3])],
               state="normal",
               command=lambda: self.moving(int(surrounding_faces[3]))).grid(row=2, column=0,
                                                                            padx=40)  # left

    def reset_cube(self):
        for i in range(3):
            for j in range(3):
                self.faces["green"][i][j] = self.Cols[0]
        for i in range(3):
            for j in range(3):
                self.faces["blue"][i][j] = self.Cols[1]
        for i in range(3):
            for j in range(3):
                self.faces["white"][i][j] = self.Cols[2]
        for i in range(3):
            for j in range(3):
                self.faces["yellow"][i][j] = self.Cols[3]
        for i in range(3):
            for j in range(3):
                self.faces["red"][i][j] = self.Cols[4]
        for i in range(3):
            for j in range(3):
                self.faces["orange"][i][j] = self.Cols[5]
        self.opt_entry.delete(0, END)
        self.selected = 0
        self.show_cube_face()

    # Solves the current state of the cube
    def generate_solution(self):
        try:
            solution = kociemba.solve(self.current_state())
            if solution == self.solved:
                self.opt_entry.delete(0, END)
                self.opt_entry.insert(0, "Cube already solved")
            else:
                self.opt_entry.delete(0, END)
                self.opt_entry.insert(0, solution)
        except:
            self.opt_entry.delete(0, END)
            self.opt_entry.insert(0, "INVALID CUBE INPUT")

    def timer_solution(self):
        try:
            if self.timer.timer_running:  # Check if the timer is running
                solution = kociemba.solve(self.current_state())
                if solution == self.solved:
                    minutes = self.timer.elapsed_time // 60
                    seconds = self.timer.elapsed_time % 60
                    elapsed_time = f"{minutes:02d}:{seconds:02d}"
                    messagebox.showinfo("Your time was", str(elapsed_time))
                    print(elapsed_time)
                    self.insert_value_into_database(elapsed_time)
                else:
                    messagebox.showerror("Error", "Cube not solved")
            else:
                messagebox.showwarning("Warning", "Timer is not running yet")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "INVALID CUBE INPUT, Reset Cube To Continue...")

    def insert_value_into_database(self, elapsed_time):#function to insert the time into the database
        conn = sqlite3.connect("rubixcubesolver.db")
        cur = conn.cursor()
        username = self.username
        print(username, elapsed_time)
        cur.execute("INSERT INTO Leaderboard VALUES(?, ?)", (username, elapsed_time))#paremeters to be inserted into the database
        conn.commit()
        conn.close()

    def init_moves_frame(self):
        # Frame for performing cube moves
        self.preform_Move_frame = LabelFrame(self.root, padx=35, pady=10, text="Move the cube")

        # making layout for move buttons
        row_num = 0
        col_num = 0
        for move in self.moves_list:
            ttk.Button(self.preform_Move_frame, width=2, text=move, command=lambda m=move: self.perform_move(m)).grid(
                row=row_num, column=col_num, padx=5)  # making buttons for the moves
            col_num += 1
            if col_num == 5:  # 5 buttons per row
                col_num = 0
                row_num += 1

        ttk.Button(self.preform_Move_frame, width=2, text="?", command=self.moves_info).grid(row=row_num,
                                                                                             column=col_num,
                                                                                             padx=5)

        # Grid the frame to make it visible
        self.preform_Move_frame.grid(row=3, column=1, padx=10)

    def perform_move(self, move):
        self.opt_entry.delete(0, END)#delete whatever was in the entry widget

        moves_instance = moves.Moves()
        move_function = getattr(moves_instance, move, None)  # dynamic function call to generate object of moves class
        if move_function:
            move_function()
        self.show_cube_face()

        double_turns_instance = moves.double_turns()
        double_turns_function = getattr(double_turns_instance, 'triple_and_double_turns',
                                        None)  # dynamic function call to generate object of double turns class
        if double_turns_function:
            double_turns_function(move)
        self.show_cube_face()

    # Scramble the cube with random moves
    def scramble_cube(self):
        self.opt_entry.delete(0, END)
        for _ in range(8): # Scramble the cube with 8 random moves
            move = random.choice(self.moves_list) # Select a random move from the list of moves
            self.perform_move(move)
        self.show_cube_face()  # Update the cube face

    def current_state(self): # function to get the current state of the cube
        state = "" # Initialize an empty string to store the state of the cube
        for i in self.faces["white"]:
            for j in i:
                state += self.select_text(j)
        for i in self.faces["red"]:
            for j in i:
                state += self.select_text(j)
        for i in self.faces["green"]:
            for j in i:
                state += self.select_text(j)
        for i in self.faces["yellow"]:
            for j in i:
                state += self.select_text(j)
        for i in self.faces["orange"]:
            for j in i:
                state += self.select_text(j)
        for i in self.faces["blue"]:
            for j in i:
                state += self.select_text(j)
        print(state)
        return state

    # Map the color to the corresponding face notation(pattern match) for the solver
    def select_text(self, colour):
        return {"w": "U",
                "r": "R",
                "y": "D",
                "o": "L",
                "g": "F",
                "b": "B"}.get(colour) # return the corresponding face notation for the solver

    def moves_info(self):
        # opens Moves Logic text file and inserts it into a tkinter text widget in a top level window
        moves_info = Toplevel()
        moves_info.title("Moves Logic")
        moves_info.resizable(False, False)
        file = open("Moves_logic.txt", "r")  # opens the file in read mode
        moves_logic = file.read()
        text = Text(moves_info)
        text.insert(END, moves_logic)
        text.pack()


# Main function to create the Tkinter root window and run the RubiksCubeSolver application
def main():
    root = Tk()
    app = RubiksCubeSolver(root, None)
    app.init_gui()
    root.mainloop()


# Run the main function if the script is executed directly
if __name__ == '__main__':
    main()
