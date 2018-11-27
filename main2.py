# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 4
# Scrolling Map/Camera
# Video link: https://youtu.be/3zV2ewk-IGU
import pygame as pg
import sys
import random
from os import path
from menu import *
from settings import *
from sprites import *
from tilemap import *
from jefes import * 

cuartos_totales = []
pantalla_completa = False
volumen = 0.0
pg.mixer.init()
pg.mixer.music.load('sound/Intro.mp3')
pg.mixer.music.set_volume(volumen)
pg.mixer.music.play(-1)
pygame.font.init()
fuente = pygame.font.Font('img/dejavu.ttf', 20)

class Game:
    def __init__(self):
        pg.init()
        if pantalla_completa:
            self.screen = pg.display.set_mode((WIDTH, HEIGHT),pg.FULLSCREEN)
        else:    
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
        self.cuarto_actual = None
        self.prox_cuarto = True

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.startroom = Map(path.join(self.game_folder, 'maps/StartRoom.txt'))
        self.room_item = Map(path.join(self.game_folder,'maps/room_item.txt'))
        self.room_boss = Map(path.join(self.game_folder,'maps/room_boss.txt'))
        self.mapas = ['maps/map.txt','maps/LargeRoom.txt','maps/XLargeRoom.txt','maps/Xverroom']
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
                        mapa.list_wall.add(wall)
                    if tile == '#':
                        self.puerta=Door(self,col+self.total_map_w, row+self.total_map_h)
                        mapa.list_door.add(self.puerta)
                    if tile == 'P':
                        self.player = Player(self, col, row+self.total_map_h)
                        mapa.list_player.add(self.player)
                    if tile == 'E':
                        self.enemi = Chaser(self, col+self.total_map_w, row+self.total_map_h, self.player)
                        mapa.list_enemis.add(self.enemi)
                    if tile == 'S':
                        self.enemi = SpiderWall_y(self, col+self.total_map_w, row+self.total_map_h,0,self.total_map_w)
                        mapa.list_enemis.add(self.enemi)
                    if tile == 'Z':
                        self.enemi = SpiderWall_x(self, col+self.total_map_w, row+self.total_map_h,0,self.total_map_w) 
                        mapa.list_enemis.add(self.enemi)
                    if tile=='D':
                        self.deco = Barril(self, col+self.total_map_w, row+self.total_map_h, self.lista_disparos)
                        mapa.list_wall.add(self.deco)
                    if tile=='I':
                        self.roomitem(col+self.total_map_w,row+self.total_map_h)
                        mapa.list_item.add(self.item)
                    if tile=='J':
                        self.jefes = Boss(self, col+self.total_map_w, row+self.total_map_h)
                        mapa.list_boss.add(self.jefes)
            width_ant = mapa.tilewidth    
            #self.total_map_w += width_ant
            if i == 5:
                mapa = self.room_item
            if i == 9:
                mapa = self.room_boss
            if i<=4 or i<9 and i>5:
                mapa = Map(path.join(self.game_folder,self.mapas[random.randint(0,3)]))
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
        # initialize all variables   and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.door = pg.sprite.Group()
        self.create_map(self.startroom)
        #self.create_map(self.map2)
        #self.create_map(self.room_item)
        #self.create_map(self.room_boss)
        self.cuarto_actual = cuartos_totales[self.no_cuarto_actual]
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
        self.cuarto_actual.update()
        for n in range(len(cuartos_totales)):
            if self.no_cuarto_actual == n:
                if self.prox_cuarto:
                    if self.player.rect.x >= self.cuarto_actual.width-32 and self.player.rect.x <= self.cuarto_actual.width:
                        self.no_cuarto_actual=n+1
                        self.cuarto_actual = cuartos_totales[self.no_cuarto_actual]
                        self.cuarto_actual.list_player.add(self.player)
                        self.player.x = 30
                        self.prox_cuarto = False
                        self.time_prox_cuarto = pg.time.get_ticks()
                    if self.player.rect.x <=0:
                        self.no_cuarto_actual=n-1 
                        self.cuarto_actual = cuartos_totales[self.no_cuarto_actual]
                        self.player.x = self.cuarto_actual.width-32
                        self.prox_cuarto = False
                        self.time_prox_cuarto = pg.time.get_ticks()
                else:
                    if pg.time.get_ticks() - self.time_prox_cuarto > 500:
                        self.prox_cuarto = True
        if self.player.heal<=0:
            self.quit()
        for listas in self.cuarto_actual.lists:
            for sprite in listas:
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
        texto1 = fuente.render("Vidas:"+str(self.player.heal), 0, (255, 255, 255))
        self.screen.blit(texto1, (32,32))
        for listas in self.cuarto_actual.lists:
            for sprite in listas:
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

def main():
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()

def comenzar_nuevo_juego():
    main()

def creditos():
    salir = False 
    opciones = [
        ("Volver", volver),
        ]

    screen = pygame.display.set_mode((420, 320))
    fondo = pygame.image.load("img/fondo.png").convert()
    texto1 = fuente.render("Santiago Faverio", 0, (0,0,0))
    texto2 = fuente.render("7º3", 0, (0,0,0))
    texto3 = fuente.render("Codigo de tilemap y camera:", 0, (0,0,0))
    texto4 = fuente.render("Chris Bradfield(Github)", 0, (0,0,0))
    menu = Menu(opciones)

    while not salir:

        for e in pygame.event.get():
            if e.type == QUIT:
                salir = True

        screen.blit(fondo, (0, 0))
        menu.actualizar()
        menu.imprimir(screen)
        screen.blit(texto1, (65,130))
        screen.blit(texto2, (65,160))
        screen.blit(texto3, (65,190))
        screen.blit(texto4, (65,220))
        pygame.display.flip()
        pygame.time.delay(10)


def salir_del_programa():
    exit(0)

def mostrar_opciones():
    salir = False 
    p="Pantalla completa  "+str(pantalla_completa)
    v="Volumen  "+str(volumen)
    opciones = [
        (p, pantalla_comple),
        (v, status_volumen),
        ("Volver", volver),
        ]

    pygame.font.init()
    screen = pygame.display.set_mode((420, 320))
    fondo = pygame.image.load("img/fondo.png").convert()
    menu = Menu(opciones)

    while not salir:

        for e in pygame.event.get():
            if e.type == QUIT:
                salir = True

        screen.blit(fondo, (0, 0))
        menu.actualizar()
        menu.imprimir(screen)

        pygame.display.flip()
        pygame.time.delay(10)

def pantalla_comple():
    global pantalla_completa
    if pantalla_completa:
        pantalla_completa = False
    elif not pantalla_completa:
        pantalla_completa = True
    mostrar_opciones()

def status_volumen():
    pass

def volver():
    menu()

def menu():    
    salir = False
    opciones = [
        ("Jugar", comenzar_nuevo_juego),
        ("Opciones", mostrar_opciones),
        ("Creditos", creditos),
        ("Salir", salir_del_programa)
        ]

    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((420, 320))
    fondo = pygame.image.load("img/fondo.png").convert()
    menu = Menu(opciones)

    while not salir:

        for e in pygame.event.get():
            if e.type == QUIT:
                salir = True

        screen.blit(fondo, (0, 0))
        menu.actualizar()
        menu.imprimir(screen)

        pygame.display.flip()
        pygame.time.delay(10)

menu()