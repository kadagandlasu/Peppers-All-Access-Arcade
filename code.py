#v1.1 added in button presses to game_setup function


import board
import busio
import digitalio
import displayio
import framebufferio
import rgbmatrix
import adafruit_imageload
import terminalio
from adafruit_display_text import label
from time import sleep, monotonic
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw import rotaryio
from core import *
from game import *

# Setup Matrix Display.
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=64,
    bit_depth=3,
    rgb_pins=[board.R0, board.B0, board.G0, board.R1, board.B1, board.G1],
    addr_pins=[board.ROW_A, board.ROW_B, board.ROW_C, board.ROW_D,board.ROW_E],
    clock_pin=board.CLK,
    latch_pin=board.LAT,
    output_enable_pin=board.OE,

)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)


# make screen parts. This is what will handle the graphics
screen = displayio.Group()
display.root_group = screen


# display splash screen
splash = displayio.OnDiskBitmap("/splash.bmp")
splash_screen = displayio.TileGrid(splash, pixel_shader=splash.pixel_shader)
screen.append(splash_screen)
sleep(2)
screen.remove(splash_screen)
screen.append(setup_group)

# inistialize the game play variables
p1_clicked = False
p2_clicked = False
coin_clicked = False
refresh_every = 0.5
now = monotonic()

# setup state machine to handle the different modes
state_list = ["SETUP", "CHOOSE", "INITIALIZE", "PLAY","GAME OVER"]
state = "INITIALIZE"

print("Developer Version")

# main game loop
while True:
    # buton click is latched between frames
    if not p1.value:
        p1_clicked = True
        p1_led.value = True
    if not p2.value:
        p2_clicked = True
        p2_led.value = True
    if not coin.value:
        coin_clicked = True
        coin_led.value = True


    if state == "INITIALIZE":

        now = monotonic()
        if game_group not in screen:
            screen.append(game_group)
        game_setup(p1_clicked, p1_clicked, coin_clicked)
        p1_clicked = False
        p2_clicked = False
        p1_led.value = False
        p2_led.value = False
        coin_clicked = True
        coin_led.value = True
        state = "PLAY"


    elif state == "PLAY":

        # call the new game_frame
        if now + refresh_every < monotonic():
            now = monotonic()
            if game_frame(p1_clicked, p1_clicked, coin_clicked):
                state = "GAME OVER"
            # release the button latch
            p1_clicked = False
            p2_clicked = False
            p1_led.value = False
            p2_led.value = False
            coin_clicked = True
            coin_led.value = True

    elif state == "GAME OVER":
        game_over(p1_button,p2_button, coin_button)
        p1_clicked = False
        p2_clicked = False
        p1_led.value = False
        p2_led.value = False
        coin_clicked = True
        coin_led.value = True
        state = "INITIALIZE"

    elif state == "SETUP":
        refresh_every = set_speed()
        state = "INITIALIZE"
