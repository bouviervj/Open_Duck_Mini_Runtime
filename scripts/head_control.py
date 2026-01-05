#!/bin/python

import time
from mini_bdx_runtime.sounds import Sounds
from mini_bdx_runtime.antennas import Antennas
from mini_bdx_runtime.projector import Projector
from eyes_controller import EyesController, ColorsList
import os
import serial

ALLOWED_SOUNDS = [ "beep1.wav", "beep2.wav", "happy1.wav", "happy2.wav", "happy3.wav" ]

class HeadControl:

    def __init__(self):
        self.sound_number = 0
        self.sounds = Sounds(volume=1.0, sound_directory="../mini_bdx_runtime/assets/")
        self.antennas = Antennas()
        self.projector = Projector(self.sounds)
        self.eyes_controller = EyesController()
        self.eyes_color_num = 0
        self.serial = self.init_serial()

    def init_serial(self):
        ser = serial.Serial(
            port ='/dev/serial0',
            baudrate = 115200,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout=1
        )
        return ser

    def run(self):
        try:
           print("Start head program ...")
           while True:
             rcv = self.serial.readline().decode().strip()
             if "PLAY SOUND" in rcv:
                self.sound_number +=1
                self.sounds.play(ALLOWED_SOUNDS[self.sound_number % len(ALLOWED_SOUNDS)])
             elif "TOGGLE FLASH" in rcv:
                self.projector.switch()
             elif "EYES" in rcv:
                print(f"Switch eyes colors {self.eyes_color_num}")
                self.eyes_color_num+=1
                self.eyes_controller.change_color(ColorsList[self.eyes_color_num % len(ColorsList)])
             elif "ANTENNA" in rcv:
                data = rcv.split(" ")
                self.antennas.set_position_left(float(data[2]))
                self.antennas.set_position_right(float(data[3]))
             else:
                print(rcv)
        except KeyboardInterrupt:
           print("Stopped by keyboard interrupt, exiting ...")
        finally:
           self.eyes_controller.all_lights_off()

if __name__ == "__main__":

     head_control = HeadControl()
     head_control.run()

