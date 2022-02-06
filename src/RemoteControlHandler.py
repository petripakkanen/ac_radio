import threading
from .ButtonHandler import ButtonHandler

class RemoteControlHandler(ButtonHandler):
    '''
        TODO
    '''
    def __init__(self, stream_player):
        super().__init__(stream_player, bouncetime=0)
        self.lock = threading.Lock()

    def __enter__(self):
        pass

    def on_button_state_switch(self, *args):
        self.stream_player.setNextActiveStream()
        self.lock.release()     # Release lock

    def __exit__(self):
        pass
