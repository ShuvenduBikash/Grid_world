import World
import threading
import time


def run():
    H = 10
    gamma = 0.9
    for _ in range(H):
        time.sleep(1)
        for i in range(World.y):
            for j in range(World.x):
                states = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
                for state in states:
                    if World.can_go(state) and (j, i) not in World.end_states:
                        World.V[i][j] = max(World.V[i][j], gamma * World.V[state[0]][state[1]])
                        World.render_cell_value()


if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    World.start_game()
