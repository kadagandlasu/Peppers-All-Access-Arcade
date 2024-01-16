import displayio
import random
import terminalio
from adafruit_display_text import label
from time import sleep

game_group = displayio.Group()

cowboy = displayio.OnDiskBitmap()
desert = displayio.OnDiskBitmap()

def dynam_timer():
	#timer would go something like this
	timer_time = random.randint(2,7)
	time.sleep(timer_time)

#set player score
player_1_win = false
player_2_win = false
player_1_score = 0
player_2_score = 0

#if player wins give them point
def player_score():
	global player_1_score
	global player_2_score
if player_1_win =  true:
	player_1_score += 1
if player_2_win = true:
	Player_2_score += 1

def game_setup():
    """this is called once to initialize your game features"""
    pass

def game_frame(p1_button:bool,p2_button:bool) -> bool:
    """this is called every frame, you need to update all your grame objects
        returns True when the game is over, else return false"""
    return False


def game_over():
    """this should display your game over screen with score also clean up the game_group"""
    pass

