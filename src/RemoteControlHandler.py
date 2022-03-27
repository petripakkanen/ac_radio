import threading
import falcon
from wsgiref.simple_server import make_server

import threading
import subprocess as sp

from .ButtonHandler import ButtonHandler
from .StreamPlayer import StreamPlayer
from .logger import get_logger

class RemoteControlHandler(ButtonHandler):
    '''
        TODO
    '''
    def __init__(self, stream_player, *args, **kwargs):
        super().__init__(stream_player, bouncetime=0)
        self.lock = threading.Lock()

    def __enter__(self):
        pass

    def on_button_state_switch(self, *args):
        self.stream_player.setNextActiveStream()
        self.lock.release()     # Release lock

    def __exit__(self):
        pass


class RemoteControlREST(RemoteControlHandler):
    '''
        TODO
    '''
    def __init__(self, stream_player, *args, **kwargs):
        super().__init__(stream_player, bouncetime=0)

        t = threading.Thread(target=self.start_api_server, args=args)
        t.start()

    def start_api_server(self):
        api_http = falcon.App()
        api_http.add_route('/set_status', PlayerAPICall(self.stream_player))
        with make_server('', 8000, api_http) as httpd:
            print('Serving on port 8000...')

            # Serve until process is killed
            httpd.serve_forever()

class PlayerAPICall():
    def __init__(self, player, *args, **kwargs):
        self.player = player
        self.logger = get_logger("APICall")

    def on_get(self, req, resp):
        self.player.block_play = not self.player.block_play
        self.logger.debug(req.params)
        try:
            if int(req.params['next']):
                self.player.setNextActiveStream()
                resp.media = "setNextActiveStream"
            else:
                if req.params['set_stream_id']:
                    self.player.setNextActiveStream(num=int(req.params['set_stream_id']))
                    resp.media = "setNextActiveStream"
        except Exception as e:
            self.logger.error(e)
