import displayio
import random
from sheep.SheepClass import *
import terminalio
from adafruit_display_text import label
from time import sleep

game_group = displayio.Group()

sheep = displayio.OnDiskBitmap("sheep/sheep3.bmp")
farm = displayio.OnDiskBitmap("sheep/farm.bmp")
bkgnd = displayio.TileGrid(farm, pixel_shader=farm.pixel_shader)

FIELD_W = 8
FIELD_H = 7

sheep_field = displayio.TileGrid(
    sheep,
    pixel_shader=sheep.pixel_shader,
    width=FIELD_W,
    height=FIELD_H,
    tile_width=8,
    tile_height=8,
)
sheep_field.pixel_shader.make_transparent(29)
sheep_field.y = 8

the_dog = Dog(2, 2)
the_sheeps = []
game_score = 0
game_tick = 0


def shake_sheep(qty: int):
    """clears sheepfield and adds qty new sheep"""
    # clear all the sheep
    for row in range(FIELD_W):
        for col in range(FIELD_H):
            sheep_field[row, col] = 0
    # add the dog
    sheep_field[the_dog.x, the_dog.y] = the_dog.angle + 4
    for s in range(qty):
        good_sheep = False
        while not good_sheep:
            sheep_x = random.randint(0, FIELD_W - 1)
            sheep_y = random.randint(0, FIELD_H - 1)
            if sheep_field[sheep_x, sheep_y] == 0:
                the_sheeps.append(Sheep(sheep_x, sheep_y))
                sheep_field[sheep_x, sheep_y] = 1
                good_sheep = True


def draw_sheep():
    # clear all the sheep
    for row in range(FIELD_W):
        for col in range(FIELD_H):
            sheep_field[row, col] = 0
    # add the dog
    sheep_field[the_dog.x, the_dog.y] = the_dog.angle + 4
    for baa in the_sheeps:
        sheep_field[baa.x, baa.y] = 1
        sheep_field[baa.x, baa.y] = 1


def score_sheep(sheep_index:int):
    global game_score
    # check for pen
    if (the_sheeps[sheep_index].x == 3 and the_sheeps[sheep_index].y == 0) and (the_dog.x in [1, 2, 3, 4, 5] and the_dog.y in [0, 1, 2]):
        the_sheeps.pop(sheep_index)
        game_score += 1


def run_sheep():
    """if sheep are within one of dog then they will shift away from dog"""
    global game_score
    # global the_sheeps
    move_check = [-1, 1]

    for i, s in enumerate(the_sheeps):
        # if the sheep is in the same place as a dog, move the sheep out of the way
        if s.x == the_dog.x and s.y == the_dog.y:
            the_sheeps[i].x += random.choice(move_check)
            the_sheeps[i].y += random.choice(move_check)
        # adjust the sheep away from the dog
        if s.x == the_dog.x - 1 and s.y == the_dog.y - 1:
            the_sheeps[i].x -= 1
            the_sheeps[i].y -= 1
        elif s.x == the_dog.x - 1 and s.y == the_dog.y:
            the_sheeps[i].y -= 1
        elif s.x == the_dog.x - 1 and s.y == the_dog.y + 1:
            the_sheeps[i].x -= 1
            the_sheeps[i].y += 1
        elif s.x == the_dog.x and s.y == the_dog.y - 1:
            the_sheeps[i].y -= 1
        elif s.x == the_dog.x and s.y == the_dog.y + 1:
            the_sheeps[i].y += 1
        elif s.x == the_dog.x + 1 and s.y == the_dog.y - 1:
            the_sheeps[i].x += 1
            the_sheeps[i].y -= 1
        elif s.x == the_dog.x + 1 and s.y == the_dog.y:
            the_sheeps[i].y += 1
        elif s.x == the_dog.x + 1 and s.y == the_dog.y + 1:
            the_sheeps[i].x += 1
            the_sheeps[i].y += 1

        # check for edges
        score_sheep(i)
        if s.x < 0:
            s.x = 0
            s.y += random.choice(move_check)

        if s.x > 7:
            s.x = 7
            s.y += random.choice(move_check)

        if s.y < 0:
            s.y = 0
            s.x += random.choice(move_check)
            if s.x < 0:
                s.x = 0
            if s.x > 7:
                s.x = 7
        if s.y > 6:
            s.y = 6
            s.x += random.choice(move_check)
            if s.x < 0:
                s.x = 0
            if s.x > 7:
                s.x = 7



def game_setup():
    """this is called once to initialize your game features"""
    global game_tick
    shake_sheep(6)
    game_group.append(bkgnd)
    game_group.append(sheep_field)
    game_tick = 0

def game_frame(p1_button:bool,p2_button:bool) -> bool:
    """this is called every frame, you need to update all your grame objects
        returns True when the game is over, else return false"""
    global game_tick
    if not p1_button:
        the_dog.turn()
        print(the_dog.angle)
    else:
        the_dog.move()
        game_tick += 1
    run_sheep()
    draw_sheep()
    print(game_tick)
    if len(the_sheeps) > 0 and game_tick < 60:
        return False
    else:
        return True


def game_over():
    """this should display your game over screen with score also clean up the game_group"""
    global game_score
    global game_tick
    global the_sheeps

    game_group.remove(sheep_field)
    game_score = (game_score * 1000)// game_tick
    text = "Score=" + str(game_score)
    font = terminalio.FONT
    color = 0x3F3F74
    text_area = label.Label(font, text=text, color=color)
    text_area.x = 4
    text_area.y = 24
    game_group.append(text_area)
    sleep(5)
    game_group.remove(text_area)
    game_group.remove(bkgnd)
    the_sheeps = []
    the_dog.x = 2
    the_dog.y = 2

