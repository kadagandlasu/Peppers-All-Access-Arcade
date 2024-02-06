import displayio
import random
import terminalio
from adafruit_display_text import label
import time

game_group = displayio.Group()

#imports desert, cowboys, and dynamite aseprite graphics
cowboys = displayio.OnDiskBitmap("western/cowboys.bmp")
dynamite = displayio.OnDiskBitmap("western/dynamite2.bmp")
desert = displayio.OnDiskBitmap("western/desert.bmp")

#creates desert, cowboys, and dynamite tilegrids
desert = displayio.TileGrid(desert, pixel_shader = desert.pixel_shader)

cowboy1 = displayio.TileGrid(
    cowboys,
    pixel_shader = cowboys.pixel_shader,
    width = 1,
    height = 1,
    tile_width = 32,
    tile_height = 32
)
cowboy1.pixel_shader.make_transparent(10)
cowboy1.y = 34
cowboy1.x = -5

cowboy2 = displayio.TileGrid(
    cowboys,
    pixel_shader = cowboys.pixel_shader,
    width = 1,
    height = 1,
    tile_width = 32,
    tile_height = 32
)
cowboy2.pixel_shader.make_transparent(10)
cowboy2.x = 40
cowboy2.y = 31

dynamite = displayio.TileGrid(
    dynamite,
    pixel_shader = dynamite.pixel_shader,
    width = 1,
    height = 1,
    tile_width = 32,
    tile_height = 32
)
dynamite.pixel_shader.make_transparent(10)
dynamite.x = 16
dynamite.y = 4


def set_comp_react():
    """randomizes computer reaction time"""
    global comp_react
    comp_react = random.randint(1,3)


def win_animate(cowboy1_win:bool,cowboy2_win:bool):
    """animates sprites according to which cowboy wins"""
    #sprite animations when cowboy 1 wins
    if cowboy1_win == True and cowboy2_win == False:
        if start_animate == frame_count:
            cowboy1.x -= 3
            cowboy1[0] = 1
        if start_animate + 4 == frame_count:
            cowboy1[0] = 2
            cowboy2.x -= 5
            cowboy2[0] = 10
        if start_animate + 8 == frame_count:
            dynamite[0] = 2
            cowboy2.x += 4
            cowboy2.y += 2
            cowboy2[0] = 11
            cowboy1[0] = 1
        if start_animate + 12 == frame_count:
            cowboy1.x -= 3
            cowboy1.y -= 1
            cowboy1[0] = 3
    #sprite animations when cowboy 2 wins
    elif cowboy1_win == False and cowboy2_win == True:
        if start_animate == frame_count:
            cowboy2.x -= 1
            cowboy2.y += 1
            cowboy2[0] = 7
        if start_animate + 4 == frame_count:
            cowboy2.x -= 7
            cowboy2.y -= 1
            cowboy2[0] = 8
            cowboy1.y += 1
            cowboy1[0] = 4
        if start_animate + 8 == frame_count:
            dynamite[0] = 2
            cowboy1.x += 3
            cowboy1.y += 2
            cowboy1[0] = 5
            cowboy2.x += 7
            cowboy2.y += 1
            cowboy2[0] = 7
        if start_animate + 12 == frame_count:
            cowboy2.x -= 4
            cowboy2.y -= 1
            cowboy2[0] = 9



def set_score():
    """sets score to cowboys according to who wins each round"""
    global cowboy1_score
    global cowboy2_score
    if cowboy1_win == True and cowboy2_win == False:
        cowboy1_score += 1
    elif cowboy1_win == False and cowboy2_win == True:
        cowboy2_score += 1

#declares and initializes scores, player count
cowboy1_score = 0
cowboy2_score = 0
cowboy_count = -1

#sets up text box for future use
text = "                   "
font = terminalio.FONT
color = 0x0000FF
text_area = label.Label(font, text = text, color = color)
text_area.x = 3
text_area.y = 5

def game_setup(p1_button:bool,p2_button:bool,coin_button:bool):
    """graphics are added to the screen and variables for frame recording, win conditions, and scorekeeping are set up"""
    global frame_count
    global comp_react
    global explode_frame
    global past_cowboy1_score
    global past_cowboy2_score
    global cowboy1_win
    global cowboy2_win
    global start_animate
    #adding graphics
    #game_group.append(desert)
    game_group.append(dynamite)
    game_group.append(cowboy1)
    game_group.append(cowboy2)
    game_group.append(text_area)
    #declaring and initializing variables related to frames, scores, and winning
    frame_count = 0
    comp_react = -1
    explode_frame = -1
    past_cowboy1_score = -1
    past_cowboy2_score = -1
    cowboy1_win = False
    cowboy2_win = False
    start_animate = -1
def game_frame(p1_button:bool,p2_button:bool,coin_button:bool) -> bool:
    """asks for player county, and repeats a round until a cowboy wins twice (best out of 3)"""
    global frame_count
    global comp_react
    global explode_frame
    global past_cowboy1_score
    global past_cowboy2_score
    global cowboy1_win
    global cowboy2_win
    global start_animate
    global cowboy_count
    #reset variables for frames, winning, and scorekeeping before each round
    if frame_count == 0:
        cowboy1[0] = 0
        cowboy2[0] = 6
        dynamite[0] = 0
        set_comp_react()
        explode_frame = random.randint(4,12)
        past_cowboy1_score = cowboy1_score
        past_cowboy2_score = cowboy2_score
        cowboy1_win = False
        cowboy2_win = False
        start_animate = -1
        cowboy1.y = 34
        cowboy1.x = -5
        cowboy2.x = 40
        cowboy2.y = 31
    #begin counting frames once player count is selected
    if cowboy_count == 1 or cowboy_count == 2:
    	frame_count += 1
    #asks for player count
    if cowboy_count != 1 and cowboy_count != 2:
        text_area.text = " PLAYERS" + "\nP1:1  P2:2"
        if p1_button:
            text_area.text = ""
            cowboy_count = 1
        elif p2_button:
            text_area.text = ""
            cowboy_count = 2
    #starts singleplayer round
    elif cowboy_count == 1:
	#if either score hasn't increased yet, stay in the round
        if cowboy1_score != past_cowboy1_score + 1 or cowboy2_score != past_cowboy2_score + 1:
	    #explode dynamite after certain number of frames, check input and animate according to fastest cowboy
            if frame_count >= explode_frame:
                if cowboy1_win == False and cowboy2_win == False:
                    dynamite[0] = 1
                    if p1_button:
                        cowboy1_win = True
                        start_animate = frame_count
                        win_animate(True,False)
                    elif frame_count >= explode_frame + comp_react:
                        cowboy2_win = True
                        start_animate = frame_count
                        win_animate(False, True)
                elif cowboy1_win == True:
                    win_animate(True, False)
                    if cowboy1[0] == 3:
                        set_score()
                elif cowboy2_win == True:
                    win_animate(False, True)
                    if cowboy2[0] == 9:
                        set_score()
    #starts mulitplayer round
    elif cowboy_count == 2:
    #if either score hasn't increased yet, stay in the round
        if cowboy1_score != past_cowboy1_score + 1 or cowboy2_score != past_cowboy2_score + 1:
	#explode dynamite after certain number of frames, check input and animate according to fastest cowboy
            if frame_count >= explode_frame:
                if cowboy1_win == False and cowboy2_win == False:
                    dynamite[0] = 1
                    if p1_button:
                        cowboy1_win = True
                        start_animate = frame_count
                        win_animate(True,False)
                    elif p2_button:
                        cowboy2_win = True
                        start_animate = frame_count
                        win_animate(False, True)
                elif cowboy1_win == True:
                    win_animate(True, False)
                    if cowboy1[0] == 3:
                        set_score()
                elif cowboy2_win == True:
                    win_animate(False, True)
                    if cowboy2[0] == 9:
                        set_score()
    #check if a cowboy has won (best of 3)
    if cowboy1_score == 2 or cowboy2_score == 2:
        return True
    #reset frame_count before starting another round
    if cowboy1_score == past_cowboy1_score + 1 or cowboy2_score == past_cowboy2_score + 1:
        frame_count = 0
    return False


def game_over(p1_button:bool,p2_button:bool,coin_button:bool):
    """remove sprites, display score and cowboy winner, remove text and background, and reset variables"""
    global cowboy1_score
    global cowboy2_score
    global player_count
    #remove cowboys and dynamite
    game_group.remove(cowboy1)
    game_group.remove(cowboy2)
    game_group.remove(dynamite)
    #display score and cowboy winner
    text_area.y = 31
    text_area.x = 17
    text_area.text = str(cowboy1_score) + " - " + str(cowboy2_score)
    time.sleep(3)
    text_area.x = 2
    text_area.y = 26
    if cowboy1_score == 2:
    	text_area.text = " COWBOY 1" + "\n   WINS"
    elif cowboy2_score == 2:
        text_area.text = " COWBOY 2" + "\n   WINS"
    time.sleep(3)
    #remove test and background while resetting score,and player count variables
    game_group.remove(text_area)
    #game_group.remove(desert)
    cowboy1_score = 0
    cowboy2_score = 0
    cowboy_count = -1



