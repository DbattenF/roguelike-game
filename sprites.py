import pygame as pg
from settings import *
import math
import random
from copy import copy

DIRECCIONES = ['UP','DOWN','RIGHT','LEFT']
dir_dig = ['downleft','downright']
dir_dige = ['upleft','upright']

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.heal = 3
        self.damage = 2
        self.dead = False
        self.can_dis = 0
        self.delay = 0
        self.time = 10
        self.can = 0
        self.o = 0
        self.x1 = 0
        self.y1 = 0
        self.colision = True
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.items = ''

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def shot(self):
        keys = pg.key.get_pressed()
        if self.items == 'ds':
            self.can = 1
            self.time = 15
        if self.can_dis<=0:
            if keys[pg.K_w]:
                if self.can == 0:
                    self.x1 = 10.5
                while(self.o <= self.can): 
                    disparo = Disparo(self.game,self.rect.x+self.x1,self.rect.y+self.y1,self,"up",self.game.lista_paredes,self.game.lista_enemigos)
                    self.game.lista_disparos.add(disparo)
                    if self.can>0:
                        self.x1 +=19
                    self.o+=1
                self.x1 = 0
                self.y1 = 0
                self.o=0
                self.can_dis+=1
            if keys[pg.K_s]:
                if self.can==0:
                    self.x1=10.5
                while(self.o <= self.can):
                    self.y1 = 25.5
                    disparo = Disparo(self.game,self.rect.x+self.x1,self.rect.y+self.y1,self,"down",self.game.lista_paredes,self.game.lista_enemigos)
                    self.game.lista_disparos.add(disparo)
                    if self.can>0:
                        self.x1 += 19
                    self.o+=1
                self.o=0
                self.x1 = 0
                self.y1 = 0
                self.can_dis+=1
            if keys[pg.K_a]:
                if self.can <= 0:
                    self.y1 = 10.5
                while(self.o <= self.can):
                    disparo = Disparo(self.game,self.rect.x+self.x1,self.rect.y+self.y1,self,"left",self.game.lista_paredes,self.game.lista_enemigos)
                    self.game.lista_disparos.add(disparo)
                    if self.can > 0:
                        self.y1+=19
                    self.o+=1
                self.x1 = 0
                self.y1 = 0
                self.o=0
                self.can_dis+=1
            if keys[pg.K_d]:
                if self.can <=0:
                    self.y1 = 10.5
                while(self.o <= self.can):
                    self.x1 = 19
                    disparo = Disparo(self.game,self.rect.x+self.x1,self.rect.y+self.y1,self,"right",self.game.lista_paredes,self.game.lista_enemigos)
                    self.game.lista_disparos.add(disparo)
                    self.o+=1
                    if self.can > 0:
                        self.y1 +=19
                self.o=0
                self.x1 = 0
                self.y1 = 0
                self.can_dis+=1
        else:
            if self.delay>=self.time:
                self.can_dis=0
                self.delay=0
            else:
                self.delay+=1

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
            hits = pg.sprite.spritecollide(self, self.game.door, True)
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
            hits = pg.sprite.spritecollide(self, self.game.door, True)   

        lista_enemigos = pg.sprite.spritecollide(self,self.game.lista_enemigos,False)

        for enemy in lista_enemigos:
            if self.colision:
                self.heal -= enemy.damage
                self.colision = False
                self.colision_time = pg.time.get_ticks()
            else:
                if pg.time.get_ticks() - self.colision_time > 1500:
                    self.colision = True
        if self.heal <=0:
            self.kill()

    def update(self):
        self.get_keys()
        self.shot()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('wall.png')#pg.Surface((TILESIZE,TILESIZE))
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.door
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.target = game.player
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Chaser(pg.sprite.Sprite):
    def __init__(self, game, x, y, target):
        self.groups = game.all_sprites, game.lista_enemigos
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('chase.png')
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.heal = 3
        self.damage = 1
        self.colision = True
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.target = target
        self.speed = 3

    def movement_wall(self):
        self.vx, self.vy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y 
        dist = math.hypot(self.vx, self.vy)
        if dist == 0:
            dist = 1
        else:
            self.vx, self.vy = self.vx / dist, self.vy / dist

    def collide_with_walls(self, dir):
        hitse = pg.sprite.collide_rect(self,self.target)
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:   
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.movement_wall()
        self.rect.x += self.vx * self.speed
        self.collide_with_walls('x')
        self.rect.y += self.vy * self.speed
        self.collide_with_walls('y')

class SpiderWall_y(pg.sprite.Sprite):
    def __init__(self, game, x, y,dire,mapa):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.heal = 2
        self.damage = 0
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 3
        self.direccion = 'DOWN'


    def _avance(self):
        if self.direccion == 'UP':
            self.vy = -self.speed
            self.vx = 0
        elif self.direccion == 'DOWN':
            self.vy = self.speed
            self.vx = 0
        elif self.direccion == 'RIGTH': 
            self.vx = self.speed
            self.vy = 0
        elif self.direccion == 'LEFT': 
            self.vx = -self.speed
            self.vy = 0
            
    def mover(self):
        hits = pg.sprite.spritecollide(self,self.game.walls,False)
        if hits:
            direccion_actual = DIRECCIONES.index(self.direccion)
            if direccion_actual == 0:
                self.direccion = DIRECCIONES[direccion_actual + 1]
            elif direccion_actual == 1:
                self.direccion = DIRECCIONES[direccion_actual - 1]

        self._avance()
        


    def update(self):
        self.mover()
        self.rect.x += self.vx
        self.rect.y += self.vy
        
class SpiderWall_x(pg.sprite.Sprite):
    def __init__(self, game, x, y,dire,mapa):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.heal = 2
        self.damage = 0
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 3
        self.direccion = 'LEFT'


    def _avance(self):
        if self.direccion == 'UP':
            self.vy = -self.speed
            self.vx = 0
        elif self.direccion == 'DOWN':
            self.vy = self.speed
            self.vx = 0
        elif self.direccion == 'RIGHT': 
            self.vx = self.speed
            self.vy = 0
        elif self.direccion == 'LEFT': 
            self.vx = -self.speed
            self.vy = 0
            
    def mover(self):
        hits = pg.sprite.spritecollide(self,self.game.walls,False)
        
        if hits:
            direccion_actual = DIRECCIONES.index(self.direccion)
            if direccion_actual == 2:
                self.direccion = DIRECCIONES[direccion_actual + 1]
            if direccion_actual == 3:
                self.direccion = DIRECCIONES[direccion_actual - 1]
        self._avance()

    def update(self):
        self.mover()
        self.rect.x += self.vx
        self.rect.y += self.vy

class Disparo(pg.sprite.Sprite):

    def __init__(self, game, x, y,target,direccion,paredes,enemigos):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('bala.png')
        self.rect = self.image.get_rect()
        self.v_disparo = 0
        self.damage = self.game.player.damage
        self.rect.y = y
        self.rect.x = x
        self.can_reb = 0
        self.dir = direccion
        self.target = target
        self.enemigos = enemigos


    def setup_damage(self):
        if self.target.items=='ps':
            self.game.player.damage = 1

    def d_up(self):
        self.rect.top -= 5
    def d_down(self):
        self.rect.bottom += 5
    def d_right(self):
        self.rect.right += 5
    def d_left(self):
        self.rect.left -= 5

    def dir_disparo(self):
        if self.dir=="up":
            self.d_up()
        if self.dir=="down":
            self.d_down()
        if self.dir=="right":
            self.d_right()
        if self.dir=="left":
            self.d_left()

    def update(self):
        self.setup_damage()
        self.dir_disparo()
        self.colision()

    def colision(self):
        lista_paredes = pg.sprite.spritecollide(self,self.game.walls,False)
        lista_enemigos = pg.sprite.spritecollide(self,self.enemigos,False)
        lista_door = pg.sprite.spritecollide(self,self.game.door,False)
        self.dir_ant = self.dir
        for i in lista_paredes:
            if self.target.items=='bs':
                if self.can_reb>=4:
                    self.kill()
                self.can_reb+=1
                if self.dir_ant=='up':
                    self.dir='down'
                elif self.dir_ant=='down':
                    self.dir='up'
                elif self.dir_ant=='right':
                    self.dir='left'
                elif self.dir_ant=='left':
                    self.dir='right'
    
            else:
                self.kill()

        for i in lista_door:
            self.kill()

        for i in lista_enemigos:
            #mport pdb;pdb.set_trace()
            j = i.__repr__()
            if self.target.items=='ps':
                pass
            else:
                if j == '<Disparos sprite(in 3 groups)>' or j == '<chase sprite(in 3 groups)>':
                    pass
                else:
                    self.kill()

            j = i.__repr__()
            if j == '<Disparos sprite(in 3 groups)>' or j == '<chase sprite(in 3 groups)>':
                pass
            else:
                i.heal -= self.damage
                if i.heal == 0:
                    i.kill()

class DoubleShot(pg.sprite.Sprite):

    def __init__(self, game, x, y,target):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32,32))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.target = target

    def colision(self):
        hits = pg.sprite.collide_rect(self,self.target)
        if hits:
            self.kill()
            self.target.items='ds'
            print("sadasd")

    def update(self):
        self.colision()

class BouncingShot(pg.sprite.Sprite):

    def __init__(self, game, x, y,target):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32,32))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.target = target

    def colision(self):
        hits = pg.sprite.collide_rect(self,self.target)
        if hits:
            self.kill()
            self.target.items='bs'

    def update(self):
        self.colision()

class Penetring(pg.sprite.Sprite):

    def __init__(self, game, x, y,target):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32,32))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.target = target

    def colision(self):
        hits = pg.sprite.collide_rect(self,self.target)
        if hits:
            self.kill()
            self.target.items='ps'

    def update(self):
        self.colision()

class Barril(pg.sprite.Sprite):

    def __init__(self, game, x, y, disparo):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('barrel.png')
        self.rect = self.image.get_rect()
        self.heal = 1
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.lista = disparo

    def colision(self):
        hits = pg.sprite.spritecollide(self,self.lista,False)
        for i in hits:
            self.kill()
        

    def update(self):
        self.colision()
