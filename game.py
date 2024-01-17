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

cowboy1 = displayio.TileGrid(cowboy_sprites, pixel_shader = cowboy_sprites.pixel_shader, 
                             width = 32, height = 32, 
                             tile_width = 6, tile_height = 2)

cowboy2 = displayio.TileGrid(cowboy_sprites, pixel_shader = cowboy_sprites.pixel_shader,
                             width = 32, height = 32,
                             tile_width = 6, tile_height = 2)

dynamite = displayio.TileGrid(dynamite_sprites, pixel_shader = dynamite_sprites.pixel_shader,
                              width = 32, height = 32,
                              tile_width = 2, tile_height = 1)
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
    
        

    
def timer():
    seconds = random.randint(2,5)
    time.sleep(seconds)





def game_setup():
    """this is called once to initialize your game features"""
    game_group.append(bkgnd)
    game_group.append(cowboy1)
    game_group.append(cowboy2)
    game_group.append(dynamite)
    

def game_frame(p1_button:bool,p2_button:bool) -> bool:
    """this is called every frame, you need to update all your grame objects
        returns True when the game is over, else return false"""
    if cowboy_count != 1 or cowboy_count != 2:
        player_count(p1_button,p2_button)
    if diff_setting != "casual" or diff_setting != "challenging":
        difficulty(p1_button,p2_button)
    
    return False


def game_over():
    """this should display your game over screen with score also clean up the game_group"""
    pass

