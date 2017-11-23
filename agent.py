import World
import threading
import time


def run():
    print(World.V)


if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    World.start_game()
