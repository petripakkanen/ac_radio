import RPi.GPIO as GPIO
from .ButtonHandler import ButtonHandler

class RpiButtonHandler(ButtonHandler):
    def __init__(self, pin, *args, **kwargs):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)

        self.pin:int = pin
        self.lastpinval = self.get_input_pin_value()
        # TODO FIXME
        super().__init__(args[0], kwargs["edge"], kwargs["bouncetime"])

        GPIO.add_event_detect(pin, GPIO.RISING, callback=self)

    def get_input_pin_value(self):
        return GPIO.input(self.pin)

    def on_button_state_switch(self, *args):
        pinval = self.get_input_pin_value()
        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.stream_player.btn_change(args)
            # self.func(*args)

        self.lastpinval = pinval
        self.lock.release()     # Release lock
