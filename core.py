import board
from adafruit_seesaw.seesaw import Seesaw
from adafruit_seesaw.digitalio import DigitalIO
from adafruit_seesaw import rotaryio
from adafruit_simplemath import map_range
import terminalio
from adafruit_display_text import label
import digitalio
import displayio
import time
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)

#core graphics variables
setup_group = displayio.Group()
menu_main_color = 0x3F3F74
menu_fill_color = 0x000000
menu_outline_color = 0x222222


# initialize peripherals
i2c = board.I2C()  # uses board.SCL and board.SDA
# setup encoder


# setup arcade buttons
arcade_qt = Seesaw(i2c, addr=0x3A)

p1 = DigitalIO(arcade_qt, 18)
p1.direction = digitalio.Direction.INPUT
p1.pull = digitalio.Pull.UP
p1_led = DigitalIO(arcade_qt, 12)
p1_led.direction = digitalio.Direction.OUTPUT

p2 = DigitalIO(arcade_qt, 19)
p2.direction = digitalio.Direction.INPUT
p2.pull = digitalio.Pull.UP
p2_led = DigitalIO(arcade_qt, 13)
p2_led.direction = digitalio.Direction.OUTPUT

coin = DigitalIO(arcade_qt, 20)
coin.direction = digitalio.Direction.INPUT
coin.pull = digitalio.Pull.UP
coin_led = DigitalIO(arcade_qt, 0)
coin_led.direction = digitalio.Direction.OUTPUT


def set_speed() -> float:
    """test progress bar to set game"""
    global last_position
    working_speed = 50
    progress_bar = HorizontalProgressBar(
        (2, 20), (60, 10),
        direction=HorizontalFillDirection.LEFT_TO_RIGHT,
        min_value=0, max_value=100, bar_color=menu_main_color, fill_color = menu_fill_color, outline_color = menu_outline_color)
    header = label.Label(terminalio.FONT,text="Speed",color=menu_main_color)
    header.x = 2
    header.y = 12

    setup_group.append(progress_bar)
    setup_group.append(header)



    # map the working_speed to fractions of a second
    setup_group.remove(progress_bar)
    setup_group.remove(header)
    fractional_speed = map_range(working_speed, 1, 100, 2, 0.0167)
    return fractional_speed

def set_controller(player: int):
    """lets you assign controllers to each player"""
    pass


def set_game() -> str:
    """chooses which game to play (if it works)"""
    return game_choice
