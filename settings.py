import pygame as pg
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACKRED = (109, 1, 1)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#Carga de imagenes
IMG_BALA = pg.image.load('img/bala.png')
IMG_BALA_CHASER = pg.image.load('img/bala_chaser.png')
IMG_BARREL = pg.image.load('img/barrel.png')
IMG_CHASE = pg.image.load('img/chase.png')
IMG_WALL = pg.image.load('img/wall.png')

# Player settings
PLAYER_SPEED = 300
