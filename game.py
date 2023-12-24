import displayio

game_group = displayio.Group()




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

