
from timeit import default_timer as timer
from datetime import timedelta
from .logger import get_logger
from .Configuration import Configuration
import mpv

class StreamPlayer():
    '''
        Class that handles stream playing and changing
        By default:
        if allowed bluetooth device is connected
         stream playing stops until all allowed bt clients is disconnected
         ^ Feature to use playing device as internet radio and bluetooth speaker
    '''
    def __init__(self, active_stream_id = -1, config_file = "config.json", simulation=False):
        self.active_stream_id = active_stream_id       # default is last stream
        # self.lastindex = self.active_stream_id
        self.config_file = config_file
        self.config = Configuration.read_config_file(config_file)
        self.streams = self.config["streams"]
        for i in range(len(self.streams)-1):
            self.streams[i]["id"] = i
        self.stream_urls = self.config["stream_urls"]
        self.prestreams = self.config["prestreams"]
        self.bluetooth = None
        self.playing = None
        self.block_play = True      # Functinality that multiple sources can output to same destination
        self.stream_change_pending = True

        if not simulation:
            self.player = mpv.MPV(ytdl=True)     # ytdl = Youtube downloader to support m3u8
        else:
            self.player = {}
        self.logger = get_logger("StreamPlayer")

    def setNextActiveStream(self, num=-1):

        # if num given set use it as id keys
        # TODO functionality used by custom playlists
        if num == -1:
            self.active_stream_id += abs(num)
        else:
            self.active_stream_id = num
        # Limit to streams length 0 to n
        if self.active_stream_id > len(self.streams) - 1:
            self.active_stream_id = 0
        elif self.active_stream_id < 0:
            self.active_stream_id = len(self.streams) - 1
        self.stream_change_pending = True

        self.logger.debug(f"Set next active stream to {self.active_stream_id}")
        # while self.active_stream_id == self.lastindex:
        #    self.active_stream_id = random.randint(0,len(self.streams)-1)
        # self.lastindex = self.active_stream_id
        # return index

    def play(self):
        t1 = timer()
        if self.stream_change_pending or not self.playing:
            self.block_play = True
            try:
                # Find and play prestream before changing to actual stream
                _player = mpv.MPV(ytdl=True)
                for index, prestream in enumerate(self.prestreams):
                    for key in prestream.keys():
                        if key == self.streams[self.active_stream_id]["prestream"]:
                            _player.play(self.prestreams[self.active_stream_id][key])

                self.player.quit()  # kill previous player
                _player.wait_for_playback()  # Wait until prestream is finished
                self.player = _player   # re-use player

                # FIXME Update config to use urls as dicts so one config only refers via key to urls
                #  > similiar solution than with prestreams
                for index, stream in enumerate(self.stream_urls):
                    for key in stream.keys():
                        if key == self.streams[self.active_stream_id]["stream_url"]:
                            #_player.play(stream[key])
                            self.player.play(self.stream_urls[self.active_stream_id][key])    # Play actual stream
                # player.wait_for_playback()    # USE WITH CAUTION
                self.playing = True
                self.stream_change_pending = False
            except Exception as e:
                self.logger.error("Validate config -file")
                self.logger.error(e)
                return e
                self.block_play = False
        self.block_play = False
        return timedelta(seconds=timer()-t1)

    def btn_change(self, *args):
        self.setNextActiveStream()
        #self.play()
