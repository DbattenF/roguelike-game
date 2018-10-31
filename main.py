# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 4
# Scrolling Map/Camera
# Video link: https://youtu.be/3zV2ewk-IGU
import pygame as pg
import sys
import random
from os import path
from settings import *
from sprites import *
from tilemap import *
from jefes import * 

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.lista_disparos = pg.sprite.Group()
        self.lista_enemigos = pg.sprite.Group()
        self.lista_paredes = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.boss_activo = False

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.map2 = Map(path.join(game_folder,'map.txt'))
        self.room_item = Map(path.join(game_folder,'room_item.txt'))
        self.room_boss = Map(path.join(game_folder,'room_boss.txt'))
        self.total_map_w = 0
        self.total_map_h = 0
        self.previous_w = 0
        self.previous_h = 0

    def create_map(self,mapa):
        for row, tiles in enumerate(mapa.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    wall=Wall(self, col+self.total_map_w, row)
                    self.lista_paredes.add(wall)
                    self.walls.add(wall)
                if tile == '#':
                    self.puerta=Door(self,col+self.total_map_w, row)
                    self.g = self.puerta.rect.left
                    self.coorx,self.coory = self.puerta.rect.x,self.puerta.y
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'E':
                    self.enemi = Chaser(self, col+self.total_map_w, row, self.player)
                    self.lista_enemigos.add(self.enemi)
                if tile == 'S':
                    self.enemi = SpiderWall_y(self, col+self.total_map_w, row,0,self.total_map_w)
                    self.lista_enemigos.add(self.enemi)
                if tile == 'Z':
                    self.enemi = SpiderWall_x(self, col+self.total_map_w, row,0,self.total_map_w) 
                    self.lista_enemigos.add(self.enemi)
                if tile=='D':
                    self.deco = Barril(self, col+self.total_map_w, row, self.lista_disparos)
                    self.lista_enemigos.add(self.deco)
                if tile=='I':
                    self.roomitem(col+self.total_map_w,row)
                if tile=='J':
                    self.jefes = Boss(self, col+self.total_map_w, row)
                    self.lista_enemigos.add(self.jefes)

        self.total_map_w += mapa.tilewidth
        self.total_map_h += mapa.tileheight
        self.previous_h = mapa.tileheight
        self.previous_w = mapa.tilewidth

    def roomitem(self,x,y):
        self.id_item = random.randint(0,2)
        if self.id_item==0:
            self.item = DoubleShot(self,x,y,self.player)
        elif self.id_item==1:
            self.item = BouncingShot(self,x,y,self.player)
        elif self.id_item==2:
            self.item = Penetring(self,x,y,self.player)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.door = pg.sprite.Group()
        self.create_map(self.map)
        self.create_map(self.map2)
        self.create_map(self.room_item)
        self.create_map(self.room_boss)
        self.mapwitdh=self.map.width+self.map2.width+self.room_item.width+self.room_boss.width
        self.mapheight=self.map.height+self.map2.height+self.room_item.height+self.room_boss.height
        self.camera = Camera(self.mapwitdh,self.mapheight)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        for sprite in self.all_sprites:
            if sprite.__repr__()=='<Boss sprite(in 2 groups)>':
                if self.boss_activo:
                    sprite.update()
                    if self.jefes.heal<=1:
                        time.sleep(0.5)
                        self.quit()
                else:
                    if self.player.rect.right >= self.g :
                        self.boss_activo = True
                if self.player.heal<=0:
                    self.quit()
            elif sprite.__repr__()=='<Lifebar sprite(in 1 groups)>':
                pass
            else:
                sprite.update()

        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()   
                """
                if event.key == pg.K_w:
                    if self.player.items == 'ds':
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y,self.player,"up",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                        disparo = Disparo(self,self.player.rect.x+20,self.player.rect.y,self.player,"up",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                    else:
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y,self.player,"up",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                if event.key == pg.K_s:
                    if self.player.items == 'ds':
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y,self.player,"down",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                        disparo = Disparo(self,self.player.rect.x+20,self.player.rect.y,self.player,"down",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                    else:
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y,self.player,"down",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                if event.key == pg.K_d:
                    if self.player.items == 'ds':
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y,self.player,"right",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y+20,self.player,"right",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                    else:
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y,self.player,"right",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                if event.key == pg.K_a:
                    if self.player.items == 'ds':
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y,self.player,"left",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y+20,self.player,"left",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                    else:
                        disparo = Disparo(self,self.player.rect.x,self.player.rect.y,self.player,"left",self.lista_paredes,self.lista_enemigos)
                        self.lista_disparos.add(disparo)
                """

    def show_start_screen(self):
        #import pdb; pdb.set_trace()
        pass

    def show_go_screen(self):
        pass

# create the game object
def main():
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
main()