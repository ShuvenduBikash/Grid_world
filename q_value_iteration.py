import World
import threading
import time


def max_a(state):
    if state in World.end_states:
        return World.R[state]

    max_val = World.Q[(state, 'u')]
    max_val = max(max_val, World.Q[(state, 'r')])
    max_val = max(max_val, World.Q[(state, 'd')])
    max_val = max(max_val, World.Q[(state, 'l')])
    return max_val


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

    if World.can_go(new_state):
        return new_state
    else:
        return state


def run():
    World.render_cell_value()
    H = 10
    gamma = 0.9
    noise = 0.2
    for _ in range(H):
        time.sleep(.1)

        Q = {}
        for state in World.states:
            for action in ['u', 'l', 'd', 'r']:
                # take this action with high probability
                high_prob = (1 - noise)
                Q[(state, action)] = high_prob * (World.R[state] + gamma * max_a(next_state(state, action)))

                low_prob = noise/3
                for other in action:
                    if other != action:
                        Q[(state, action)] += low_prob * (World.R[state] + gamma * max_a(next_state(state, other)))

        World.Q = Q
        World.render_q_values()


if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    World.start_game()
