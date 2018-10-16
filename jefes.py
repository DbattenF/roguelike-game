import pygame as pg
from settings import *
import time
import math

DIRECCIONES = ['UP','DOWN','RIGHT','LEFT']

class Boss(pg.sprite.Sprite):
	def __init__(self, game, x, y):
	    self.groups = game.all_sprites
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = pg.Surface((128, 128))
	    self.image.fill(LIGHTGREY)
	    self.rect = self.image.get_rect()
	    self.vx, self.vy = 0, 0
	    self.heal = 50
	    self.rect.x = x * TILESIZE
	    self.rect.y = y * TILESIZE
	    self.speed = 3
	    self.direccion = 'LEFT'
	    self.items=''
	    self.lista_player = pg.sprite.Group()
	    self.lista_player.add(self.game.player)

	def disparo(self):
		disparo = Disparos(self.game,self.rect.x,self.rect.y,self.game.walls,self.lista_player)
		self.game.lista_disparos.add(disparo)


	def update(self):
		self.disparo()
		self.rect.x += self.vx
		self.rect.y += self.vy


class Disparos(pg.sprite.Sprite):
	cambio_x = 0
	cambio_y = 0

	def __init__(self, game, x, y,paredes,enemigos):
	    self.groups = game.all_sprites
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = pg.image.load('bala.png')
	    self.rect = self.image.get_rect()
	    self.v_disparo = 0
	    self.damage = 1
	    self.vx, self.vy = 0,0
	    self.rect.y = y
	    self.rect.x = x
	    self.target = game.player
	    self.paredes = paredes
	    self.enemigos = enemigos


	def setup_damage(self):
	    if self.target.items=='ps':
	        self.damage = 0.25

	def d_up(self):
	    self.rect.top -= 5
	def d_down(self):
	    self.rect.bottom += 5
	def d_right(self):
	    self.rect.right += 5
	def d_left(self):
	    self.rect.left -= 5

	def movement_wall(self):
		self.vx, self.vy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y 
		dist = math.hypot(self.vx, self.vy)
		if dist == 0:
		    dist = 1
		else:
		    self.vx, self.vy = self.vx / dist, self.vy / dist

	def update(self):
	    print(self.target.items)
	    self.setup_damage()
	    self.movement_wall()
	    self.rect.x += self.vx * 5
	    self.rect.y += self.vy * 5 
	    self.colision()

	def colision(self):
	    lista_paredes = pg.sprite.spritecollide(self,self.paredes,False)
	    lista_enemigos = pg.sprite.spritecollide(self,self.enemigos,False)
	    for i in lista_paredes:
	        self.kill()

	    for i in lista_enemigos:
	        if self.target.items=='ps':
	            pass
	        else:
	            self.kill()
	        i.heal -= self.damage
	        if i.heal ==0:
	            i.kill()