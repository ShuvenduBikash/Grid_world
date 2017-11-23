from tkinter import *

master = Tk()


# defining the grid size
(x, y) = (4, 3)
Width = 100  # Width of a grid
player = (0, y - 1)  # position of the player
restart = False
score = 1
walk_reward = -0.04
render_cell_ = True

board = Canvas(master, width=x * Width, height=y * Width)
walls = [(1, 1)]
specials = [(3, 1, "red", -1), (3, 0, "green", 1)]
V = [[0 for i in range(x)] for j in range(y)]
for s in specials:
    V[s[1]][s[0]] = s[3]

text = Label(master, height=1, width=18)
text.config(text = "Score: 1", font="Times 25")


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


def render_cell_value():
    for i in range(y):
        for j in range(x):
            if (i, j) not in walls:
                board.create_text(j * Width + Width / 2, i * Width + Width / 2, fill="blue", font="Times 20",
                              text=V[i][j])


def try_move(dx, dy):
    global player, x, y, score, walk_reward, me, restart
    if restart:
        restart_game()
    # update score
    score += walk_reward
    text.config(text="Score: {:.6f}".format(score))
    print("score: ", score)

    # update the coordinate of agent
    new_x = player[0] + dx
    new_y = player[1] + dy
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x * Width + Width * 2 / 10, new_y * Width + Width * 2 / 10, new_x * Width + Width * 8 / 10,
                     new_y * Width + Width * 8 / 10)
        player = (new_x, new_y)

        if render_cell_:
            render_cell_value()

    # handle the special grids
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score += walk_reward
            score += w
            if score > 0:
                print("Success! score: ", score)
            else:
                print("Fail! score: ", score)
            restart = True
            return
            # print "score: ", score


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart
    player = (0, y - 1)
    score = 1
    restart = False
    board.coords(me, player[0] * Width + Width * 2 / 10, player[1] * Width + Width * 2 / 10,
                 player[0] * Width + Width * 8 / 10, player[1] * Width + Width * 8 / 10)


# bind action to keys
master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0] * Width + Width * 2 / 10, player[1] * Width + Width * 2 / 10,
                            player[0] * Width + Width * 8 / 10, player[1] * Width + Width * 8 / 10, fill="orange",
                            width=1, tag="me")

board.grid(row=0, column=0)
text.grid(row=1, column=0)


def start_game():
    master.mainloop()


if __name__ == '__main__':
    master.mainloop()
