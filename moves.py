from cube import face, green, blue, white, yellow, red, orange  # Import face and colour constants from the cube module


class Moves():
    def R(self):
        face[red][:] = face[red][::-1]
        face[red][:] = face[red].transpose()
        # transposing them to flip the face using numpy manipulation, as these are only single turn moves the degree
        # of movement only needs to be 90
        tempg = [face[green][0][2], face[green][1][2], face[green][2][2]]
        tempw = [face[white][0][2], face[white][1][2], face[white][2][2]]
        tempb = [face[blue][2][0], face[blue][1][0], face[blue][0][0]]
        tempy = [face[yellow][0][2], face[yellow][1][2], face[yellow][2][2]]

        tempw, tempb, tempy, tempg = tempg, tempw, tempb, tempy  # the surrounding faces cubes are stored in
        # temporary lists and swapped so that the whole cube can be updated accordingly

        face[green][0][2], face[green][1][2], face[green][2][2] = tempg[0], tempg[1], tempg[2]  # assigning the new
        # elements to the faces from there temporary list
        face[white][0][2], face[white][1][2], face[white][2][2] = tempw[0], tempw[1], tempw[2]
        # e.g green cubies will be replaced with white ones

        face[blue][2][0], face[blue][1][0], face[blue][0][0] = tempb[0], tempb[1], tempb[2]
        face[yellow][0][2], face[yellow][1][2], face[yellow][2][2] = tempy[0], tempy[1], tempy[2]

    def L(self):
        face[orange][:] = face[orange][::-1]
        face[orange][:] = face[orange].transpose()

        tempg = [face[green][0][0], face[green][1][0], face[green][2][0]]
        tempw = [face[white][0][0], face[white][1][0], face[white][2][0]]
        tempb = [face[blue][2][2], face[blue][1][2], face[blue][0][2]]
        tempy = [face[yellow][0][0], face[yellow][1][0], face[yellow][2][0]]

        tempw, tempb, tempy, tempg = tempb, tempy, tempg, tempw

        face[green][0][0], face[green][1][0], face[green][2][0] = tempg[0], tempg[1], tempg[2]
        face[white][0][0], face[white][1][0], face[white][2][0] = tempw[0], tempw[1], tempw[2]
        face[blue][2][2], face[blue][1][2], face[blue][0][2] = tempb[0], tempb[1], tempb[2]
        face[yellow][0][0], face[yellow][1][0], face[yellow][2][0] = tempy[0], tempy[1], tempy[2]

    def U(self):
        face[white][:] = face[white][::-1]
        face[white][:] = face[white].transpose()

        tempg = [face[green][0][0], face[green][0][1], face[green][0][2]]
        tempo = [face[orange][0][0], face[orange][0][1], face[orange][0][2]]
        tempb = [face[blue][0][0], face[blue][0][1], face[blue][0][2]]
        tempr = [face[red][0][0], face[red][0][1], face[red][0][2]]

        tempg, tempo, tempb, tempr = tempr, tempg, tempo, tempb

        face[green][0][0], face[green][0][1], face[green][0][2] = tempg[0], tempg[1], tempg[2]
        face[orange][0][0], face[orange][0][1], face[orange][0][2] = tempo[0], tempo[1], tempo[2]
        face[blue][0][0], face[blue][0][1], face[blue][0][2] = tempb[0], tempb[1], tempb[2]
        face[red][0][0], face[red][0][1], face[red][0][2] = tempr[0], tempr[1], tempr[2]

    def D(self):
        face[yellow][:] = face[yellow][::-1]
        face[yellow][:] = face[yellow].transpose()

        tempg = [face[green][2][0], face[green][2][1], face[green][2][2]]
        tempo = [face[orange][2][0], face[orange][2][1], face[orange][2][2]]
        tempb = [face[blue][2][0], face[blue][2][1], face[blue][2][2]]
        tempr = [face[red][2][0], face[red][2][1], face[red][2][2]]

        tempg, tempo, tempb, tempr = tempo, tempb, tempr, tempg

        face[green][2][0], face[green][2][1], face[green][2][2] = tempg[0], tempg[1], tempg[2]
        face[orange][2][0], face[orange][2][1], face[orange][2][2] = tempo[0], tempo[1], tempo[2]
        face[blue][2][0], face[blue][2][1], face[blue][2][2] = tempb[0], tempb[1], tempb[2]
        face[red][2][0], face[red][2][1], face[red][2][2] = tempr[0], tempr[1], tempr[2]

    def F(self):
        face[green][:] = face[green][::-1]
        face[green][:] = face[green].transpose()

        tempw = [face[white][2][0], face[white][2][1], face[white][2][2]]
        tempo = [face[orange][2][2], face[orange][1][2], face[orange][0][2]]
        tempy = [face[yellow][0][0], face[yellow][0][1], face[yellow][0][2]]
        tempr = [face[red][0][0], face[red][1][0], face[red][2][0]]

        tempw, tempo, tempy, tempr = tempo, tempy, tempr, tempw

        face[white][2][0], face[white][2][1], face[white][2][2] = tempw[0], tempw[1], tempw[2]
        face[orange][0][2], face[orange][1][2], face[orange][2][2] = tempo[0], tempo[1], tempo[2]
        face[yellow][0][2], face[yellow][0][1], face[yellow][0][0] = tempy[0], tempy[1], tempy[2]
        face[red][0][0], face[red][1][0], face[red][2][0] = tempr[0], tempr[1], tempr[2]

    def B(self):
        face[blue][:] = face[blue][::-1]
        face[blue][:] = face[blue].transpose()

        tempw = [face[white][0][0], face[white][0][1], face[white][0][2]]
        tempo = [face[orange][0][0], face[orange][1][0], face[orange][2][0]]
        tempy = [face[yellow][2][2], face[yellow][2][1], face[yellow][2][0]]
        tempr = [face[red][0][2], face[red][1][2], face[red][2][2]]

        tempw, tempo, tempy, tempr = tempr, tempw, tempo, tempy

        face[white][0][0], face[white][0][1], face[white][0][2] = tempw[0], tempw[1], tempw[2]
        face[orange][2][0], face[orange][1][0], face[orange][0][0] = tempo[0], tempo[1], tempo[2]
        face[yellow][2][0], face[yellow][2][1], face[yellow][2][2] = tempy[0], tempy[1], tempy[2]
        face[red][0][2], face[red][1][2], face[red][2][2] = tempr[0], tempr[1], tempr[2]


class double_turns(Moves):  # inheriting the moves class and making a child class for double and triple turns

    def get_move_function(self, move_char):  # creating a dictionary for the double and triple turns
        # the function returns contains a dictionary with the double and triple turn moves as key values and returns
        # their corresponding function
        move_dict = {"R'": self.R, "L'": self.L, "U'": self.U, "D'": self.D, "F'": self.F, "B'": self.B,
                     'R2': self.R, 'L2': self.L, 'U2': self.U, 'D2': self.D, 'F2': self.F, 'B2': self.B}
        return move_dict.get(move_char)

    def triple_and_double_turns(self, move_char):  # this function gets the key value and then preforms the move
        move_function = self.get_move_function(move_char)  # creating a varible move_function and assinging it to the
        # function, this gets the corresponding move to its key value
        if move_char[-1] == "'":  # if triple turn move (ends in ') then preforms the move three times
            for i in range(3):
                move_function()
        elif move_char[-1] == "2":  # if double turns move (ends in 2) preforms move 3 times
            for i in range(2):
                move_function()
