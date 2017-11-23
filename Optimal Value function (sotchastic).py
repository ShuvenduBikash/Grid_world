import World
import threading
import time


def run():
    World.render_cell_value()
    H = 10
    gamma = 0.9
    for _ in range(100):
        new_V = [[0 for i in range(World.x)] for j in range(World.y)]

        time.sleep(.1)
        for i in range(World.y):
            for j in range(World.x):

                if (j, i) not in World.end_states:
                    states = [(i + 1, j), (i, j + 1), (i - 1, j), (i, j - 1)]
                    new_val = -100000

                    for k in range(len(states)):
                        state_val = World.R[i][j]
                        state = states[k]
                        state_l = states[(k - 1) % len(states)]
                        state_r = states[(k + 1) % len(states)]

                        if World.can_go(state):
                            y_, x_ = state
                            state_val += 0.8 * (0.9 * World.V[y_][x_])

                        if World.can_go(state_l):
                            y_, x_ = state_l
                            state_val += 0.1 * (0.9 * World.V[y_][x_])

                        if World.can_go(state_r):
                            y_, x_ = state_r
                            state_val += 0.1 * (0.9 * World.V[y_][x_])

                        new_val = max(new_val, state_val)

                    new_V[i][j] = new_val

                else:
                    new_V[i][j] = World.R[i][j]

        World.V = new_V
        World.render_cell_value()




if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    World.start_game()
