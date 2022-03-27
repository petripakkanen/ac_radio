'''
    Modded Tivoli audio radio code
	GPIO 9 Channel A
	GPIO 11 Channel B
'''
import time
import falcon

from .BTClient import BTClient
from .Configuration import Configuration
from .StreamPlayer import StreamPlayer
from .RpiButtonHandler import RpiButtonHandler
from .logger import get_logger
from .RemoteControlHandler import RemoteControlREST

encoder_ch_a = 9
encoder_ch_b = 11

player = StreamPlayer()

btn_a = RpiButtonHandler(encoder_ch_a, player, edge='rising', bouncetime=100)
btn_b = RpiButtonHandler(encoder_ch_b, player, edge='rising', bouncetime=100)

btn_a.start()
btn_b.start()

logger = get_logger("Main")

# bluetooth enabled
player.bluetooth = BTClient()

# REST api enabled
http_api = RemoteControlREST(player)

while 1:
    # Top level logic
    # When bluetooth is connected, stop networkstream
    # and when it's disconnected continue networkstream
    # FIXME LOGIC when changing between sources
    try:
        if player.bluetooth.is_connected():
            if player.playing is True and not player.block_play:
                logger.info("Bluetooth connected and player is playing")
                logger.info("Player quit()..")
                player.player.quit()
                player.playing = False
        else:
            #if player.playing:
            #    player.player.quit()
            # Logic with pre-stream functionality
            if (((player.playing is False or player.playing is None) and not player.block_play) and not player.stream_change_pending) or player.stream_change_pending:
                logger.info("Player play()..")
                player.play()
                if player.stream_change_pending:  # Stream change pending
                    player.stream_change_pending = False
    except Exception as e:
        logger.error(e)
    time.sleep(0.1)
