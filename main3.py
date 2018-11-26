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

cuartos_totales = []

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
        self.lista_door = pg.sprite.Group()
        self.disparos_enemigos = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.boss_activo = False
        self.pos_ran = 0
        self.no_cuarto_actual = 0

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.startroom = Map(path.join(game_folder, 'maps/StartRoom.txt'))
        self.map = Map(path.join(game_folder,'maps/map.txt'))
        self.room_item = Map(path.join(game_folder,'maps/room_item.txt'))
        self.room_boss = Map(path.join(game_folder,'maps/room_boss.txt'))
        self.largeroom = Map(path.join(game_folder,'maps/LargeRoom.txt'))
        self.xlargeroom = Map(path.join(game_folder,'maps/XLargeRoom.txt'))
        self.mapas = [self.map,self.largeroom,self.xlargeroom]
        self.total_map_w = 0
        self.total_map_h = 0
        self.previous_w = 0
        self.previous_h = 0

    def create_map(self,mapa):
        i=0
        while i<=10:
            cuartos_totales.append(mapa)
            for row, tiles in enumerate(mapa.data):
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        wall=Wall(self, col+self.total_map_w, row+self.total_map_h)
                        self.lista_paredes.add(wall)
                        self.walls.add(wall)
                    if tile == '#':
                        self.puerta=Door(self,col+self.total_map_w, row+self.total_map_h)
                        self.lista_door.add(self.puerta)
                        self.coorx,self.coory = self.puerta.rect.x,self.puerta.y
                    if tile == 'P':
                        self.player = Player(self, col, row+self.total_map_h)
                    if tile == 'E':
                        self.enemi = Chaser(self, col+self.total_map_w, row+self.total_map_h, self.player)
                        self.lista_enemigos.add(self.enemi)
                    if tile == 'S':
                        self.enemi = SpiderWall_y(self, col+self.total_map_w, row+self.total_map_h,0,self.total_map_w)
                        self.lista_enemigos.add(self.enemi)
                    if tile == 'Z':
                        self.enemi = SpiderWall_x(self, col+self.total_map_w, row+self.total_map_h,0,self.total_map_w) 
                        self.lista_enemigos.add(self.enemi)
                    if tile=='D':
                        self.deco = Barril(self, col+self.total_map_w, row+self.total_map_h, self.lista_disparos)
                        self.lista_enemigos.add(self.deco)
                    if tile=='I':
                        self.roomitem(col+self.total_map_w,row+self.total_map_h)
                    if tile=='J':
                        self.jefes = Boss(self, col+self.total_map_w, row+self.total_map_h)
                        self.lista_enemigos.add(self.jefes)
            self.pos_ran = random.randint(0,1)
            self.pos_map = random.randint(0,2)
            if self.pos_ran == 0:
                width_ant = mapa.tilewidth    
                self.total_map_w += width_ant
                if i == 5:
                    mapa = self.room_item
                if i == 9:
                    mapa = self.room_boss
                if i<=4 or i<9 and i>5:
                    mapa = self.mapas[self.pos_map]
                i+=1
            elif self.pos_ran == 1:
                height_ant = mapa.tileheight
                self.total_map_h += mapa.tileheight
                if i == 5:
                    mapa = self.room_item
                if i == 9:
                    mapa = self.room_boss
                if i<=4 or i<9 and i>5:
                    mapa = self.mapas[self.pos_map]
                i+=1
                       
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
        self.create_map(self.startroom)
        #self.create_map(self.map2)
        #self.create_map(self.room_item)
        #self.create_map(self.room_boss)
        print(cuartos_totales)
        self.camera = Camera(10000,10000)

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
        #print(self.clock)
        cuarto_actual = cuartos_totales[self.no_cuarto_actual]
        if self.player.rect.x>300:
            self.no_cuarto_actual = 1
        if self.player.rect.y>300:
            self.no_cuarto_actual = 2
        if self.player.heal<=0:
            self.quit()
        for sprite in self.all_sprites:
            if sprite.__repr__()=='<Boss sprite(in 2 groups)>':
                if self.boss_activo:
                    sprite.update()
                    if self.jefes.heal<=1:
                        time.sleep(0.5)
                        self.quit()
                else:
                    if pg.sprite.collide_rect(self.player,self.puerta) :
                        self.boss_activo = True
            elif sprite.__repr__()=='<Lifebar sprite(in 1 groups)>':
                pass
            else:
                sprite.update()
        print(cuarto_actual)
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