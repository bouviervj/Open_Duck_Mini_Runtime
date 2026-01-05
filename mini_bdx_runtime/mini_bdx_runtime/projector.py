import board
import digitalio
import time
from .sounds import Sounds

PROJECTOR_GPIO = board.D25

SOUND_NAME = "lamp2.wav"

class Projector:
    def __init__(self, sounds: Sounds):
        self.project = digitalio.DigitalInOut(PROJECTOR_GPIO)
        self.project.direction = digitalio.Direction.OUTPUT
        self.sounds = sounds
        self.on = False

    def switch(self):
        self.on = not self.on

        if self.on:
           self.sounds.play(SOUND_NAME, True)
        else:
           self.sounds.stop(SOUND_NAME)

        self.project.value = self.on

    def stop(self):
        self.project.value = False
        self.project.deinit()


if __name__ == "__main__":
    p = Projector()
    try:
        while True:
            p.switch()
            time.sleep(1)
    finally:
        p.stop()
