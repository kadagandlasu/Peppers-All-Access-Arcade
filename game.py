import displayio
import random
import terminalio
from adafruit_display_text import label
from time import sleep

game_group = displayio.Group()

cowboy_sprites = displayio.OnDiskBitmap("western/western.bmp")
dynamite_sprites = displayio.OnDiskBitmap("western/dynamite.bmp")
desert = displayio.OnDiskBitmap("western/desert.bmp")

bkgnd = displayio.TileGrid(desert, pixel_shader = desert.pixel_shader)

cowboy1 = displayio.TileGrid(
    cowboy_sprites, 
    pixel_shader = cowboy_sprites.pixel_shader,                 
    width = 32, 
    height = 32, 
    tile_width = 6, tile_height = 2
)

cowboy2 = displayio.TileGrid(
    cowboy_sprites, 
    pixel_shader = cowboy_sprites.pixel_shader,
    width = 32, 
    height = 32,
    tile_width = 6, 
    tile_height = 2
)

dynamite = displayio.TileGrid(
    dynamite_sprites, 
    pixel_shader = dynamite_sprites.pixel_shader,
    width = 32, 
    height = 32,
    tile_width = 4, 
    tile_height = 1
)

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
    

def comp_react(seconds:int) -> bool:
    if diff_setting == "casual":
        seconds += random.randint(2,3)
    elif diff_setting == "challenging":
        seconds += random.randint(1,2)
    time.sleep(seconds)
    return True


def win_animate(cowboy1_win:bool,cowboy2_win:bool):
    if cowboy1_win == True and cowboy2_win == False:
        cowboy1[0] = 1
        time.sleep(0.25)
        cowboy1[0] = 2
        time.sleep(0.5)
        cowboy2[0] = 4
        dynamite[0] = 2
        time.sleep(0.25)
        cowboy2[0] = 5
        cowboy1[0] = 1
        time.sleep(0.25)
        dynamite[0] = 3
        time.sleep(0.25)
        cowboy1[0] = 3
    elif cowboy1_win == False and cowboy2_win == True:
        cowboy2[0] = 1
        time.sleep(0.25)
        cowboy2[0] = 2
        time.sleep(0.5)
        cowboy1[0] = 4
        dynamite[0] = 2
        time.sleep(0.25)
        cowboy1[0] = 5
        cowboy2[0] = 1
        time.sleep(0.25)
        dynamite[0] = 3
        time.sleep(0.25)
        cowboy2[0] = 3
    


def game_setup():
    """this is called once to initialize your game features"""
    game_group.append(bkgnd)
    game_group.append(cowboy1)
    game_group.append(cowboy2)
    game_group.append(dynamite)
    

def game_frame(p1_button:bool,p2_button:bool) -> bool:
    """this is called every frame, you need to update all your game objects
        returns True when the game is over, else return false"""
    cowboy1[0] = 0
    cowboy2[0] = 6
    if cowboy_count != 1 or cowboy_count != 2:
        player_count(p1_button,p2_button)
    if diff_setting != "casual" or diff_setting != "challenging":
        difficulty(p1_button,p2_button)
    if cowboy_count == 1:
        seconds = random.randint(2,5)
        comp_button = comp_react(seconds)
        time.sleep(seconds)
        dynamite[0] = 1
        if p1_button:
            def win_animate(True,False)
        elif comp_button:
            def win_animate(False, True)
    elif cowboy_count == 2:
        time.sleep(random.randint(2,5))
        dynamite[0] = 1
        if p1_button:
            def win_animate(True,False)
        elif p2_button:
            def win_animate(False,True)
            
    
    return False


def game_over():
    """this should display your game over screen with score also clean up the game_group"""
    pass


