# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time

import board

import neopixel_spi as neopixel

#import signal

import sys

import random

from threading import Thread

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 20

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRBW

# Standard definition for colors
BLACK = (0,0,0,0)
WHITE = (255,255,255,0)
GREEN = (0,255,0,0)
RED = (255,0,0,0)
BLUE = (0,0,255,0)
PURPLE = (255,0,255,0)
YELLOW = (255,255,0,0)
CYAN = (0,255,255,0)

ColorsList = [GREEN, RED, BLUE, PURPLE, YELLOW, CYAN]

class EyesController:

    def __init__(self):
        self.spi = board.SPI()
        self.pixels = neopixel.NeoPixel_SPI(
           self.spi, num_pixels, brightness=0.2, frequency = 6400000, auto_write=False, pixel_order=ORDER, reset_time = 0.04
        )
        self.color = CYAN
        Thread(target=self.eyes_worker, daemon=True).start()

    def __del__(self):
        # shutdown the eyes
        self.all_lights_off()

    def all_lights_off(self):
        """Sets all pixels to black and updates the strip."""
        self.pixels.fill((0, 0, 0))  # Set all pixel colors to 'off'
        self.pixels.show()           # Update the strip with the new colors

    def change_color(self, color):
        self.color = color

    def eyes_worker(self):
       rotate = 0

       try:
         while True:

           # Blink
           if (random.random()>0.99):
              self.pixels.fill(BLACK)
              self.pixels.show()
              time.sleep(0.05)


           # Left eye
           self.pixels[0] = BLACK

           rotate+=1
           #print(f"Rotate modulo {rotate % 6}  -  left: { 1+rotate%6 } - right { 5-rotate%6 + 8 }")

           self.pixels[1] = BLACK
           self.pixels[2] = BLACK
           self.pixels[3] = BLACK
           self.pixels[4] = BLACK
           self.pixels[5] = BLACK
           self.pixels[6] = BLACK

           self.pixels[rotate % 6 +1] = self.color 

           # Right eye
           self.pixels[7] = BLACK
           self.pixels[8] = BLACK
           self.pixels[9] = BLACK
           self.pixels[10] = BLACK
           self.pixels[11] = BLACK
           self.pixels[12] = BLACK
           self.pixels[13] = BLACK

           self.pixels[5-((rotate-1) % 6)+8] = self.color

           self.pixels.show()
           time.sleep(0.01)

        #rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step

       except KeyboardInterrupt:
          # This block can be removed if the signal_handler is used, 
          # but it doesn't hurt to have a fallback.
          pass

       finally:
          # This finally block ensures the lights are turned off and GPIO cleaned up
          # even if an unexpected error occurs.
          print("Cleaning up...")
          self.all_lights_off()
          print("Shutdown complete.")

if __name__ == "__main__":
     eyes_controller = EyesController()
     try:
       color_list = [CYAN, RED, GREEN, BLUE, PURPLE, YELLOW]
       color_num = 0
       while True:
          color_num+=1
          eyes_controller.change_color(color_list[color_num % 4])
          time.sleep(1)

     except KeyboardInterrupt:
        pass
     finally:
        eyes_controller.all_lights_off()
