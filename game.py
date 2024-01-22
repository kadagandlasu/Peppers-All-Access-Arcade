import displayio
import random
import terminalio
from adafruit_display_text import label
import time

game_group = displayio.Group()

cowboy_sprites = displayio.OnDiskBitmap("western/sprite_sheet.bmp")
dynamite_sprites = displayio.OnDiskBitmap("western/dynamite_sprite_sheet.bmp")
#desert = displayio.OnDiskBitmap("western/desert.bmp")

#bkgnd = displayio.TileGrid(desert, pixel_shader = desert.pixel_shader)

cowboy1 = displayio.TileGrid(
    cowboy_sprites, 
    pixel_shader = cowboy_sprites.pixel_shader,                 
    width = 32, 
    height = 32, 
    tile_width = 6, tile_height = 2
)
cowboy1.pixel_shader.make_transparent(10)

cowboy2 = displayio.TileGrid(
    cowboy_sprites, 
    pixel_shader = cowboy_sprites.pixel_shader,
    width = 32, 
    height = 32,
    tile_width = 6, 
    tile_height = 2
)
cowboy2.pixel_shader.make_transparent(10)
cowboy2.x = 32

dynamite = displayio.TileGrid(
    dynamite_sprites, 
    pixel_shader = dynamite_sprites.pixel_shader,
    width = 32, 
    height = 32,
    tile_width = 4, 
    tile_height = 1
)
dynamite.x = 25

cowboy1_score = 0
cowboy2_score = 0

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
            diff_setting "challenging"
    game_group.remove(text_area)
    

def comp_react():
    global initial
    initial = time.time()
    global seconds
    if diff_setting == "casual":
        seconds == random.randint(3,4)
    elif diff_setting == "challenging":
        seconds == random.randint(2,3)


def win_animate(cowboy1_win:bool,cowboy2_win:bool):
    if cowboy1_win == True and cowboy2_win == False:
        cowboy1[0] = 1
        time.sleep(0.25)
        cowboy1[0] = 2
        time.sleep(0.5)
        cowboy2[0] = 10
        dynamite[0] = 2
        time.sleep(0.25)
        cowboy2[0] = 11
        cowboy1[0] = 1
        time.sleep(0.25)
        cowboy1[0] = 3
    elif cowboy1_win == False and cowboy2_win == True:
        cowboy2[0] = 7
        time.sleep(0.25)
        cowboy2[0] = 8
        time.sleep(0.5)
        cowboy1[0] = 4
        dynamite[0] = 2
        time.sleep(0.25)
        cowboy1[0] = 5
        cowboy2[0] = 7
        time.sleep(0.25)
        cowboy2[0] = 9


def score(cowboy1_win:bool,cowboy2:bool):
    global cowboy1_score
    global cowboy2_score
    if cowboy1_win == True and cowboy2_win == False:
        cowboy1_score += 1
    elif cowboy1_win == False and cowboy2_win == True:
        cowboy2_score += 1
    


def dynam_timer():
	#timer would go something like this
	timer = random.randint(2,7)
	time.sleep(timer)

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
    #game_group.append(bkgnd)
    game_group.append(cowboy1)
    game_group.append(cowboy2)
    game_group.append(dynamite)
    display.root_group = game_group
    

def game_frame(p1_button:bool,p2_button:bool) -> bool:
    """this is called every frame, you need to update all your game objects
        returns True when the game is over, else return false"""
    cowboy1[0] = 0
    cowboy2[0] = 6
    dynamite[0] = 0
    if cowboy_count != 1 or cowboy_count != 2:
        player_count(p1_button,p2_button)
    if diff_setting != "casual" or diff_setting != "challenging":
        difficulty(p1_button,p2_button)
    if cowboy_count == 1:
        time.sleep(random.randint(2,5))
        comp_react()
        dynamite[0] = 1
        if p1_button:
            win_animate(True,False)
            score(True,False)
        elif time.time() == initial + seconds:
            win_animate(False, True)
            score(False,True)
    elif cowboy_count == 2:
        time.sleep(random.randint(2,5))
        dynamite[0] = 1
        if p1_button:
            win_animate(True,False)
            score(True,False)
        elif p2_button:
            win_animate(False,True)
            score(True,False)
    if cowboy1_score == 2 or cowboy2_score == 2:
        return True
    return False


def game_over():
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
    #game_group.remove(bkgnd)
    cowboy1_score = 0
    cowboy2_score = 0
    diff_setting = ""
    player_count = -1
