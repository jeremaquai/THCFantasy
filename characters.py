import arcade
from constants import WIDTH, HEIGHT


class Character(arcade.Sprite):
    def __init__(self, path, scale):
        # Call the parent class
        super().__init__(path_or_texture=path, scale=scale)

        self.name = str
        self.level = int
        self.currentXp = int
        self.xpToNextLevel = int
        self.maxHp = int
        self.currentHp = int

class Player(Character):
    def __init__(self, path, scale):
        # Call the parent class
        super().__init__(path=path, scale=scale)

        self.window_height = HEIGHT
        self.window_width = WIDTH
        self.name = 'Player'
        self.level = 1
        self.currentXp = 0
        self.xpToNextLevel = 0
        self.maxHp = 100
        self.currentHp = self.maxHp

    def update(self, delta_time = 1 / 60, *args, **kwargs):
        '''Move the player'''
        # Move player
        # check for out-of-bounds
        # if self.left < 0:
        #     self.left = 0
        # elif self.right > self.window_width - 1:
        #     self.right = self.window_width - 1

        # if self.bottom < 0:
        #     self.bottom = 0
        # elif self.top > self.window_height - 1:
        #     self.top = self.window_height - 1
