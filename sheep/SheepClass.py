class Sheep:
    def __init__(self, x_posn, y_posn):
        self.x = x_posn
        self.y = y_posn

class Dog:
    def __init__(self, x_posn, y_posn):
        self.x = x_posn
        self.y = y_posn
        self.angle = 4

    def turn(self):
        self.angle += 1
        if self.angle >= 8:
            self.angle = 0

    def move(self):
        if self.angle == 0:
            self.y -= 1
        elif self.angle == 1:
            self.x += 1
            self.y -= 1
        elif self.angle == 2:
            self.x += 1
        elif self.angle == 3:
            self.x += 1
            self.y += 1
        elif self.angle == 4:
            self.y += 1
        elif self.angle == 5:
            self.x -= 1
            self.y += 1
        elif self.angle == 6:
            self.x -= 1
        elif self.angle == 7:
            self.x -= 1
            self.y -= 1


        if self.x < 0:
            self.x = 0
        elif self.x > 7:
            self.x = 7
        if self.y < 0:
            self.y = 0
        elif self.y > 6:
            self.y = 6
