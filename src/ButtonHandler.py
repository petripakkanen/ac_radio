import threading
from .logger import get_logger

class ButtonHandler(threading.Thread):
    '''
        Base class for button handlers
        Input is hw related so pin reading is subclassed
    '''
    def __init__(self, stream_player, edge='both', bouncetime=200, **kwargs):  # bouncetime = ms
        super().__init__(daemon=True)
        self.edge = edge    # rising, falling, both
        self.bouncetime = float(bouncetime)/1000    # debounce delay, set 0 for software switch

        self.stream_player = stream_player
        self.lock = threading.Lock()
        self.logger = get_logger()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return
        # Use threading timer for debouncing
        t = threading.Timer(self.bouncetime, self.on_button_state_switch, args=args)
        t.start()

    def on_button_state_switch(self, *args):
        self.stream_player.btn_change(args)
        self.lock.release()     # Release lock


class virtualButtonHandler(ButtonHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def get_input_pin_value(self, _input_value = 1):
        return _input_value

    def on_button_state_switch(self, *args):
        raise NotImplementedError
