'''
    Modded Tivoli audio radio code
	GPIO 9 Channel A
	GPIO 11 Channel B
'''
import time

from .BTClient import BTClient
from .Configuration import Configuration
from .StreamPlayer import StreamPlayer
from .RpiButtonHandler import RpiButtonHandler
from .logger import get_logger

encoder_ch_a = 9
encoder_ch_b = 11

player = StreamPlayer()

btn_a = RpiButtonHandler(encoder_ch_a, player, edge='rising', bouncetime=100)
btn_b = RpiButtonHandler(encoder_ch_b, player, edge='rising', bouncetime=100)

btn_a.start()
btn_b.start()

logger = get_logger()

player.bluetooth = BTClient()



while 1:
    # Top level logic
    # When bluetooth is connected, stop networkstream
    # and when it's disconnected continue networkstream
    try:
        player.bluetooth.sniff_connection()
        if player.bluetooth.is_connected:
            if player.playing is True:
                logger.info("Bluetooth connected and player is playing")
                logger.info("Player quit()..")
                player.player.quit()
                player.playing = False
        else:
            #if player.playing:
            #    player.player.quit()
            if ((player.playing is False or player.playing is None) and not player.block_play) and not player.stream_change_pending:
                logger.info("Player a play()..")
                player.play()
            elif player.stream_change_pending:
                logger.info("Player s play()..")
                player.play()
                player.stream_change_pending = False
    except Exception as e:
        logger.error(e)
    time.sleep(0.1)
