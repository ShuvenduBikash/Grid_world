from tkinter import *

master = Tk()

# defining the grid size
(x, y) = (4, 3)
Width = 100             # Width of a grid
player = (0, y - 1)     # position of the player

board = Canvas(master, width=x * Width, height=y * Width)
walls = [(1, 1)]
specials = [(3, 1, "red", -1), (3, 0, "green", 1)]


def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="white", width=1)
            # temp = {}
            # for action in actions:
            #     temp[action] = create_triangle(i, j, action)
            # cell_scores[(i, j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i * Width, j * Width, (i + 1) * Width, (j + 1) * Width, fill="black", width=1)


render_grid()


me = board.create_rectangle(player[0] * Width + Width * 2 / 10, player[1] * Width + Width * 2 / 10,
                            player[0] * Width + Width * 8 / 10, player[1] * Width + Width * 8 / 10, fill="orange",
                            width=1, tag="me")


board.grid(row=0, column=0)

if __name__ == '__main__':
    master.mainloop()
