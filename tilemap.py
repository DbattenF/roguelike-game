import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        self.list_wall = pg.sprite.Group()
        self.list_floor = pg.sprite.Group()
        self.list_door = pg.sprite.Group()
        self.list_enemis = pg.sprite.Group()
        self.list_player = pg.sprite.Group()
        self.list_boss = pg.sprite.Group()
        self.list_item = pg.sprite.Group()
        self.list_disparos = pg.sprite.Group()
        self.list_enemis_disp = pg.sprite.Group()
        self.list_lifebar = pg.sprite.Group()
        self.list_drops = pg.sprite.Group()
        self.activo = True
        self.lists = [self.list_floor,self.list_drops,self.list_item,self.list_lifebar,self.list_wall,self.list_door,self.list_enemis,self.list_player,self.list_boss,self.list_disparos,self.list_enemis_disp]

    def update(self):
        print(self.activo)
        if not self.list_enemis.__nonzero__() or not self.list_enemis.__nonzero__():
            self.activo = False

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
