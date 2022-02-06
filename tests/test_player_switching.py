import os
from timeit import default_timer as timer
from datetime import timedelta
from mutagen.mp3 import MP3

from ac_radio.StreamPlayer import StreamPlayer
from ac_radio.RemoteControlHandler import RemoteControlHandler

from ac_radio.logger import get_logger
logger = get_logger()
'''
    TODO
    * test stream source changing
    * test with core modules
    * test with all module combinations
        - with module enabled run modules own tests
          and integration tests are specified in here
'''
def test_prestreams_exist():
    player = StreamPlayer(config_file="src/ac_radio/template_config.json", simulation=True)
    for prestream in player.prestreams:
        print(prestream)
        for val in prestream:
            audio = MP3(prestream[val])
            print(prestream[val], " length:", audio.info.length)
            assert os.path.isfile(prestream[val])

def test_player_stream_change_time():
    player = StreamPlayer(config_file="src/ac_radio/template_config.json", simulation=True)
    start = timer()
    logger.debug("play:", player.play(), "\n")

    stop = timer()
    logger.debug("Play() took", timedelta(seconds=stop-start))

def test_player_init():
    '''
        TODO
        Test switcing conditions
    '''
    player = StreamPlayer(config_file="src/ac_radio/template_config.json", simulation=True)
    player.playing = True
    assert player.playing

def test_remote_control_handler():
    player = StreamPlayer(config_file="src/ac_radio/template_config.json", simulation=True)
    remote_ctrl = RemoteControlHandler(player)
    remote_ctrl.start()

    n = 10000  # default playlist starting point
    '''
        Test that switching works for n switching times
        can be used for tuning switches finding optimal
        debounce time
    '''
    _pl_index = -1
    for i in range(n):
        if _pl_index > len(player.streams) - 1:
            _pl_index = 0
        elif _pl_index < 0 and i != 0:
            _pl_index = len(player.streams) -1
        assert player.active_stream_id == _pl_index
        remote_ctrl()
        _pl_index += 1
        #time.sleep(0.01)
    assert remote_ctrl
