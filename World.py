from tkinter import *

master = Tk()

# defining the grid size
(x, y) = (4, 3)
Width = 100             # Width of a grid
player = (0, y - 1)     # position of the player

board = Canvas(master, width=x * Width, height=y * Width)


def render_grid():
    global x, y
    for i in range(x):
        for j in range(y):
            pass


render_grid()

me = board.create_rectangle(player[0] * Width + Width * 2 / 10, player[1] * Width + Width * 2 / 10,
                            player[0] * Width + Width * 8 / 10, player[1] * Width + Width * 8 / 10, fill="orange",
                            width=1, tag="me")


board.grid(row=0, column=0)

if __name__ == '__main__':
    master.mainloop()
