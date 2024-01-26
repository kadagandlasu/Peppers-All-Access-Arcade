import displayio
import random
import terminalio
from adafruit_display_text import label
import time

game_group = displayio.Group()

cowboy_sprites = displayio.OnDiskBitmap("western/cowboys.bmp")
dynamite_sprites = displayio.OnDiskBitmap("western/dynamite.bmp")
desert = displayio.OnDiskBitmap("western/desert.bmp")

bkgnd = displayio.TileGrid(desert, pixel_shader = desert.pixel_shader)

cowboy1 = displayio.TileGrid(
    cowboys, 
    pixel_shader = cowboys.pixel_shader,                 
    width = 32, 
    height = 32, 
    tile_width = 6, tile_height = 2
)
cowboy1.pixel_shader.make_transparent(10)
cowboy1.y = 31

cowboy2 = displayio.TileGrid(
    cowboys, 
    pixel_shader = cowboys.pixel_shader,
    width = 32, 
    height = 32,
    tile_width = 6, 
    tile_height = 2
)
cowboy2.pixel_shader.make_transparent(10)
cowboy2.x = 31
cowboy2.y = 31

dynamite = displayio.TileGrid(
    dynamite, 
    pixel_shader = dynamite.pixel_shader,
    width = 32, 
    height = 32,
    tile_width = 4, 
    tile_height = 1
)
dynamite.pixel_shader.make_transparent(10)
dynamite.x = 15

cowboy1_score = 0
cowboy2_score = 0
cowboy_count = -1
diff_setting = ""

def player_count(p1_button:bool, p2_button:bool):
    text = "1-PLAYER      2-PLAYER"
    font = terminalio.FONT
    color = 0x0000FF
    text_area = label.Label(font, text = text, color = color)
    game_group.append(text_area)
    global cowboy_count
    if p1_button:
        cowboy_count = 1
    elif p2_button:
        cowboy_count = 2
    game_group.remove(text_area)
    

def difficulty(p1_button:bool, p2_button:bool):
    text = "CASUAL    CHALLENGING"
    font = terminalio.FONT
    color = 0x0000FF
    text_area = label.Label(font, text = text, color = color)
    game_group.append(text_area)
    global diff_setting
    if cowboy_count == 1:
        if p1_button:
            diff_setting = "casual"
        if p2_button:
            diff_setting = "challenging"
    game_group.remove(text_area)

def add_comp_frames():
    global comp_frames
    if diff_setting == "casual":
	comp_frames = random.randint(15,25)
    elif diff_setting == "challenging":
	comp_frames = random.randint(7,14)


def win_animate(cowboy1_win:bool,cowboy2_win:bool):
    if cowboy1_win == True and cowboy2_win == False:
        cowboy1[0] = 1
        cowboy1[0] = 2
        cowboy2[0] = 10
        dynamite[0] = 2
        cowboy2[0] = 11
        cowboy1[0] = 1
        cowboy1[0] = 3
    elif cowboy1_win == False and cowboy2_win == True:
        cowboy2[0] = 7
        cowboy2[0] = 8
        cowboy1[0] = 4
        dynamite[0] = 2
        cowboy1[0] = 5
        cowboy2[0] = 7
        cowboy2[0] = 9


def score(cowboy1_win:bool,cowboy2:bool):
    global cowboy1_score
    global cowboy2_score
    if cowboy1_win == True and cowboy2_win == False:
        cowboy1_score += 1
    elif cowboy1_win == False and cowboy2_win == True:
        cowboy2_score += 1


def game_setup(p1_button:bool,p2_button:bool,coin_button:bool):
    """this is called once to initialize your game features"""
    global frame_counter
    game_group.append(bkgnd)
    game_group.append(cowboy1)
    game_group.append(cowboy2)
    game_group.append(dynamite)
    frame_counter = 0

def game_frame(p1_button:bool,p2_button:bool,coin_button:bool) -> bool:
    """this is called every frame, you need to update all your game objects
        returns True when the game is over, else return false"""
    global frame_counter
    cowboy1[0] = 0
    cowboy2[0] = 6
    dynamite[0] = 0
    if cowboy_count != 1 or cowboy_count != 2:
        player_count(p1_button,p2_button)
    if diff_setting != "casual" or diff_setting != "challenging":
        difficulty(p1_button,p2_button)
    if cowboy_count == 1:
        final_frame = random.randint(10,60)
	comp_react = final_frame + comp_frames
	temp_cowboy1_score = cowboy1_score
	temp_cowboy2_score = cowboy2_score
        while True:
	    frame_count += 1
	    if frame_count < final_frame:
		continue
	    dynamite[0] = 1
	    if cowboy1_score == temp_cowboy1_score + 1 or cowboy2_score == temp_cowboy2_score + 1:
	        break
            if p1_button:
            	score(True,False)
		win_animate(True,False) 
            elif frame_count == comp_react:
                score(False,True)
		win_animate(False, True)
    elif cowboy_count == 2:
        final_frame = random.randint(10,60)
	temp_cowboy1_score = cowboy1_score
	temp_cowboy2_score = cowboy2_score
        while True:
	    frame_count += 1
	    if frame_count < final_frame:
		continue
	    dynamite[0] = 1
	    if cowboy1_score == temp_cowboy1_score + 1 or cowboy2_score == temp_cowboy2_score + 1:
	        break
            if p1_button:
            	score(True,False)
		win_animate(True,False) 
            elif p2_button:
                score(False,True)
		win_animate(False, True)
    frame_count = 0
    if cowboy1_score == 2 or cowboy2_score == 2:
        return True
    return False


def game_over(p1_button:bool,p2_button:bool,coin_button:bool):
    """this should display your game over screen with score also clean up the game_group"""
    global cowboy1_score
    global cowboy2_score
    global diff_setting
    global player_count
    
    game_group.remove(cowboy1)
    game_group.remove(cowboy2)
    game_group.remove(dynamite)
    text = str(cowboy1_score) + " - " + str(cowboy2_score)
    font = terminalio.FONT
    color = 0x0000FF
    text_area = label.Label(font, text = text, color = color)
    game_group.append(text_area)
    time.sleep(2)
    if cowboy1_score == 2:
    	text_area.text = "RED COWBOY WINS"
    elif cowboy2_score == 2:
	text_area.text = "BLUE COWBOY WINS"
    time.sleep(3)
    game_group.remove(text_area)
    game_group.remove(bkgnd)
    cowboy1_score = 0
    cowboy2_score = 0
    diff_setting = ""
    cowboy_count = -1
