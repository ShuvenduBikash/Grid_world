import World
import threading
import time


def run():
    H = 10
    gamma = 0.9
    for _ in range(H):
        time.sleep(.1)

        new_V = {}
        for state in list(World.neighbour_states.keys()):
            new_V[state] = World.R[state]

            # find all possible neighbour of this state
            neighbours = World.neighbour_states[state]

            # calculate value making each of them most probable action each time
            for neighbour in neighbours:
                state_val = (World.R[state] + gamma * World.V[neighbour])
                new_V[state] = max(new_V[state], state_val)

        World.V = new_V
        World.render_cell_value()


if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    World.start_game()
