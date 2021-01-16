from pynput.keyboard import Listener

class Handler:

    def __init__(self, keeper):
        with Listener(
            on_press=keeper.register,
            on_release=None) as listener:
            listener.join()