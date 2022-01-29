'''
    Modded Tivoli audio radio code
	GPIO 9 Channel A
	GPIO 11 Channel B
'''
import RPi.GPIO as GPIO
import threading
import mpv
import time
import random

encoder_ch_a = 9
encoder_ch_b = 11

class StreamPlayer():
    def __init__(self):
        self.index = 0
        self.lastindex = index
        self.player = mpv.MPV(ytdl=True)     # ytdl = Youtube downloader to support m3u8 


    def changeIndex(self, num):
        print("Change index", num)
        global urls
        self.index += num
        if self.index > len(urls) - 1:
            self.index = 0
        elif self.index < 0:
            self.index = len(urls) - 1

        while self.index == self.lastindex:
            self.index = random.randint(0,3)
        self.lastindex = index
        # return index

    def play(self):
        # player.playlist_clear()
        self.player.quit()
        #time.sleep(0.1)
        self.player = mpv.MPV(ytdl=True)
        #time.sleep(0.1)
        self.player.play(spks[self.index])    # Play stream info -speak ex. channel name
        self.player.wait_for_playback()  # Wait until last play is finished
        self.player.play(urls[self.index])    # Play actual stream
        # player.wait_for_playback()

    def btn_change(self):
        self.changeIndex(1)
        print("Playing url", urls[self.index])
        self.play()

    #def btn_change2():
    #    global index
    #    index = changeIndex(index, -1)
    #    print("Playing url", urls[index])
    #    play()

class ButtonHandler(threading.Thread):
    def __init__(self, pin, stream_player: StreamPlayer, edge='both', bouncetime=200):  # bouncetime = ms
        super().__init__(daemon=True)

        self.edge = edge
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return
        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.stream_player.
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()     # Release lock


urls = ['https://yleuni-f.akamaihd.net/i/yleliveradiohd_5@113882/master.m3u8',
	'https://supla.digitacdn.net/live/_definst_/supla/radioaalto/chunklist.m3u8',
	'https://c0.toivon.net/toivon/toivon_0?mp=/stream',
	'https://supla.digitacdn.net/live/_definst_/supla/radiorock/chunklist.m3u8']

spks = ['/home/pi/speakit/speak_puheradio.mp3',
	'/home/pi/speakit/speak_radioaalto.mp3',
	'/home/pi/speakit/speak_jouluradio.mp3',
	'/home/pi/speakit/speak_rokkiradio.mp3']


GPIO.setmode(GPIO.BCM)
GPIO.setup(encoder_ch_a, GPIO.IN)
GPIO.setup(encoder_ch_b, GPIO.IN)

player = StreamPlayer()

btn_a = ButtonHandler(encoder_ch_a, player, edge='rising', bouncetime=100)
btn_b = ButtonHandler(encoder_ch_b, player, edge='rising', bouncetime=100)

btn_a.start()
btn_b.start()

GPIO.add_event_detect(encoder_ch_a, GPIO.RISING, callback=btn_a)
GPIO.add_event_detect(encoder_ch_b, GPIO.RISING, callback=btn_b)

while 1:
	time.sleep(1)
