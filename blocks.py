from main import DISPLAY


from pygame import *
import os

PLATFORM_WIDTH = 26
PLATFORM_HEIGHT = 26
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("%s/blocks/platform1.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/gun.png" % ICON_DIR)