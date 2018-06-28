from tkinter import *
import tkinter.messagebox as messagebox

MAX_SIZE = 19
BLACK = 0
WHITE = 1


class GUI(Frame):
    def display_board(self, first='black'):
        self.canvas = Canvas(self, width="280m", height="280m", bg='#F7DCB4')
        self.canvas.pack(side=LEFT)

        # black starts
        self.color = first

        self.size = 50
        size = self.size
        for x in range(MAX_SIZE):
            self.canvas.create_line(size + x * size, size, size + x * size, size + 18 * size)
        for y in range(MAX_SIZE):
            self.canvas.create_line(size, size + y * size, size + 18 * size, size + size * y)

        # initialize the board
        self.board = [[-1 for _ in range(MAX_SIZE)] for _ in range(MAX_SIZE)]

        self.canvas.bind('<Button-1>', callback)
        self.pack()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        Pack.config(self)

    def change_color(self):
        if self.color == 'black':
            self.color = 'white'
        else:
            self.color = 'black'

    def update_board(self, x, y, use_dlg=False):
        offset = 15

        row = int(round(float(x) / self.size))
        column = int(round(float(y) / self.size))

        # check if legal move
        if self.check_move(row, column) == False:
            print('illegal move')
            return False
        else:
            print('next move by ' + self.color, [row, column])

        new_x = row * 50
        new_y = column * 50

        self.canvas.create_oval(new_x - offset, new_y - offset, new_x + offset,
                                new_y + offset, width=1, fill=self.color, outline='black')

        if self.color == 'black':
            self.board[row][column] = BLACK

        elif self.color == 'white':
            self.board[row][column] = WHITE

        # check if last move results in win
        if self.check_for_win(row, column):
            print(self.color + ' wins!')

            if use_dlg:
                answer = messagebox.askyesno('Game Over!', self.color + ' wins! -- New Game?')
                if answer:
                    print('yes')
                    self.reset_board()
                else:
                    print('no')
                    return False
        return True

    def check_move(self, x, y):
        if x < 0 or x >= MAX_SIZE or y < 0 or y >= MAX_SIZE:
            print('out of bounds')
            return False
        elif self.board[x][y] != -1:
            print(self.board[x][y])
            print('already occupied')
            return False
        else:
            return True

    def check_for_win(self, x, y):
        dirs = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for (dx, dy) in dirs:
            sum1 = self.check_lines(x, y, dx, dy)
            sum2 = self.check_lines(x, y, -dx, -dy)

            if sum1 + sum2 >= 5:
                return True
        return False

    def check_lines(self, x, y, dx, dy):
        count = -1  # don't count itself
        current = self.board[x][y]

        while x >= 0 and y >= 0 and x < MAX_SIZE and y < MAX_SIZE and self.board[x][y] == current:
            count = count + 1
            x = x + dx
            y = y + dy
        return count

    def reset_board(self):
        self.canvas.destroy()
        self.displayBoard()


def callback(event):
    game.update_board(event.x, event.y, False)


if __name__ == "__main__":
    game = GUI()
    game.display_board()
    game.mainloop()
