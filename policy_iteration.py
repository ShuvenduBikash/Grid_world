import World
import threading
import time


def run():
    World.render_cell_value()
    H = 10
    gamma = 0.9
    noise = 0.2
    for _ in range(H):
        time.sleep(.1)

        V = {}
        for state in list(World.neighbour_states.keys()):
            if state in World.end_states:
                V[state] = World.R[state]
                continue

            V[state] = -1000000
            # find all possible actions at this state
            all_actions = World.available_actions[state]
            for action in all_actions:
                # action = policy[state]
                state_val = 0

                high_prob = (1 - noise)
                low_prob = noise / (len(all_actions) - 1)

                state_val += high_prob * (World.R[state] + gamma * World.V[World.next_state(state, action)])

                # iterate stochastic probable state
                for other in all_actions:
                    if other != action:
                        state_val += low_prob * (World.R[state] + gamma * World.V[World.next_state(state, other)])

                if state_val >= V[state]:
                    V[state] = state_val
                    policy[state] = action

        World.V = V
        World.render_cell_value()

        # update all arrows
        for state in World.states:
            World.clear_all_arrow(state)
            World.update_arrow_color(state, policy[state])


if __name__ == '__main__':
    policy = {
        # (0, 0): 'r',
        # (0, 1): 'u',
        # (0, 2): 'u',
        # (1, 0): 'r',
        # (1, 2): 'r',
        # (2, 0): 'r',
        # (2, 1): 'u',
        # (2, 2): 'u',
        # (3, 2): 'l',
    }

    # Enabling specific grid
    World.grid_value_mode()
    World.create_arrow()

    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    World.start_game()
