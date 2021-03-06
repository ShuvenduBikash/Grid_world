from tkinter import *

master = Tk()
master.title("Grid world")

# defining the grid size
(x, y) = (4, 3)
Width = 100  # Width of a grid
player = (0, y - 1)  # position of the player
restart = False
score = 1
walk_reward = -0.04
render_me = False

cell_text = [[None for i in range(x)] for j in range(y)]
q_text = {}

board = Canvas(master, width=x * Width, height=y * Width)
walls = [(1, 1)]
specials = [(3, 1, "red", -1), (3, 0, "green", 1)]
end_states = [(3, 1), (3, 0)]
actions = ['u', 'l', 'd', 'r']

text = Label(master, height=1, width=18)
text.config(text="Score: 1", font="Times 25")

# Define value and rewards
states = []
V = {}
R = {}
neighbour_states = {}
available_actions = {}
Q = {}

for j in range(y):
    for i in range(x):
        state = (i, j)
        V[state] = 0

        if state not in walls and state not in end_states:
            states.append(state)
            R[state] = 0

for s in specials:
    state = (s[0], s[1])
    R[state] = s[3]
    V[state] = R[state]


def can_go(state):
    x_, y_ = state
    if 0 <= x_ < x and 0 <= y_ < y and (x_, y_) not in walls:
        return True
    else:
        return False


for state in states:
    i = state[0]
    j = state[1]
    neighbours = [(i + 1, j, 'r'), (i, j + 1, 'd'), (i - 1, j, 'l'), (i, j - 1, 'u')]
    possible_neighbours = []
    possible_actions = []

    for n in neighbours:
        neighbour = (n[0], n[1])
        if can_go(neighbour):
            possible_neighbours.append(neighbour)
            possible_actions.append(n[2])

    available_actions[state] = possible_actions
    neighbour_states[state] = possible_neighbours

for state in end_states:
    neighbour_states[state] = []

for state in states:
    q_values = [(state, 'u'), (state, 'r'), (state, 'd'), (state, 'l')]
    for q in q_values:
        Q[q] = 0


# print(neighbour_states)


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


def render_tringle():
    for state in states:
        i = state[0]
        j = state[1]
        board.create_line(100 * i, 100 * j, (i + 1) * 100, (j + 1) * 100)
        board.create_line((i + 1) * 100, 100 * j, 100 * i, (j + 1) * 100)


def create_q_values_text():
    for state in states:
        x_ = state[0]
        y_ = state[1]
        q_text[state] = {}
        q_text[state]['u'] = board.create_text(100 * x_ + 50, 100 * y_ + 15, fill="blue",
                                               font="Times 10", text="{:.2f}".format(Q[(state), 'u']))
        q_text[state]['r'] = board.create_text(100 * x_ + 75, 100 * y_ + 50, fill="blue",
                                               font="Times 10", text="{:.2f}".format(Q[(state), 'r']))
        q_text[state]['d'] = board.create_text(100 * x_ + 50, 100 * y_ + 85, fill="blue",
                                               font="Times 10", text="{:.2f}".format(Q[(state), 'd']))
        q_text[state]['l'] = board.create_text(100 * x_ + 25, 100 * y_ + 50, fill="blue",
                                               font="Times 10", text="{:.2f}".format(Q[(state), 'l']))

    for state in end_states:
        q_text[state] = board.create_text(state[0] * Width + Width / 2, state[1] * Width + Width / 2, fill="blue",
                                          font="Times 15",
                                          text="{:.2f}".format(R[state]))


triangle_size = 0.1
arrows = {}


def create_arrow():
    for state in states:
        i = state[0]
        j = state[1]
        arrows[state] = {}
        arrows[state]['u'] = board.create_polygon((i + 0.5 - triangle_size) * Width, (j + triangle_size) * Width,
                                                  (i + 0.5 + triangle_size) * Width, (j + triangle_size) * Width,
                                                  (i + 0.5) * Width, j * Width,
                                                  fill="white", width=1)

        arrows[state]['d'] = board.create_polygon((i + 0.5 - triangle_size) * Width, (j + 1 - triangle_size) * Width,
                                                  (i + 0.5 + triangle_size) * Width, (j + 1 - triangle_size) * Width,
                                                  (i + 0.5) * Width, (j + 1) * Width,
                                                  fill="white", width=1)

        arrows[state]['l'] = board.create_polygon((i + triangle_size) * Width, (j + 0.5 - triangle_size) * Width,
                                                  (i + triangle_size) * Width, (j + 0.5 + triangle_size) * Width,
                                                  i * Width, (j + 0.5) * Width,
                                                  fill="white", width=1)

        arrows[state]['r'] = board.create_polygon((i + 1 - triangle_size) * Width, (j + 0.5 - triangle_size) * Width,
                                                  (i + 1 - triangle_size) * Width, (j + 0.5 + triangle_size) * Width,
                                                  (i + 1) * Width, (j + 0.5) * Width,
                                                  fill="white", width=1)


def update_arrow_color(state, action, color='green'):
    board.itemconfig(arrows[state][action], fill=color)


def clear_all_arrow(state):
    for action in actions:
        board.itemconfig(arrows[state][action], fill='white')


def render_q_values():
    for state in states:
        for action in actions:
            board.itemconfig(q_text[state][action], text="{:.2f}".format(Q[(state, action)]))


def create_cell_value():
    for i in range(y):
        for j in range(x):
            if (i, j) not in walls:
                cell_text[i][j] = board.create_text(j * Width + Width / 2, i * Width + Width / 2, fill="blue",
                                                    font="Times 15",
                                                    text="{:.2f}".format(V[(j, i)]))


def render_cell_value():
    for i in range(y):
        for j in range(x):
            if (i, j) not in walls:
                board.itemconfig(cell_text[i][j], text="{:.2f}".format(V[(j, i)]))


def render_cell_reward():
    for i in range(y):
        for j in range(x):
            if (i, j) not in walls:
                board.itemconfig(cell_text[i][j], text="{:.2f}".format(R[(j, i)]))


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

if render_me:
    me = board.create_rectangle(player[0] * Width + Width * 2 / 10, player[1] * Width + Width * 2 / 10,
                                player[0] * Width + Width * 8 / 10, player[1] * Width + Width * 8 / 10, fill="orange",
                                width=1, tag="me")

board.grid(row=0, column=0)
text.grid(row=1, column=0)


def start_game():
    master.mainloop()


if __name__ == '__main__':
    master.mainloop()


def grid_value_mode():
    create_cell_value()


def q_value_mode():
    render_tringle()
    create_q_values_text()


def next_state(state, action):
    x, y = state
    if action == 'u':
        y -= 1
    elif action == 'r':
        x += 1
    elif action == 'd':
        y += 1
    elif action == 'l':
        x -= 1

    new_state = (x, y)

    if can_go(new_state):
        return new_state
    else:
        return state


def max_a(state):
    if state in end_states:
        return R[state]

    max_val = Q[(state, 'u')]
    max_val = max(max_val, Q[(state, 'r')])
    max_val = max(max_val, Q[(state, 'd')])
    max_val = max(max_val, Q[(state, 'l')])
    return max_val
