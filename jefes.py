import pygame as pg
from settings import *
import time
import math
import random

DIRECCIONES = ['UP','DOWN','RIGHT','LEFT']
dir_dis = ['up','down','right','left']

class Boss(pg.sprite.Sprite):
	def __init__(self, game, x, y):
	    self.groups = game.all_sprites
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = pg.Surface((128, 128))
	    self.image.fill(LIGHTGREY)
	    self.rect = self.image.get_rect()
	    self.vx, self.vy = 0, 0
	    self.heal = 500
	    self.rect.x = x * TILESIZE
	    self.rect.y = y * TILESIZE
	    self.speed = 3
	    self.pos = ''
	    self.direccion = 'LEFT'
	    self.items=''
	    self.can_dis=0
	    self.delay = 0
	    self.lista_player = pg.sprite.Group()
	    self.lista_player.add(self.game.player)

	def disparo(self):
			disparo = Disparos(self.game,self.rect.x,self.rect.y,self.game.walls,self.lista_player,'up',True)
			self.game.lista_disparos.add(disparo)
			disparo = Disparos(self.game,self.rect.x+96,self.rect.y,self.game.walls,self.lista_player,'up',True)
			self.game.lista_disparos.add(disparo)

	
	def hab_1(self,cant,dire):
		j=0
		pos_y = 0
		while j<=cant:
			i=0
			pos_x=0
			while i<=cant:
				i+=1
				disparo = Disparos(self.game, self.rect.x+pos_x, self.rect.y+pos_y, self.game.walls,self.lista_player,dire)
				self.game.lista_disparos.add(disparo)
				pos_x+=16
			j+=1
			pos_y+=16
		

	def update(self):
		self.pos = random.randint(0,6)
		if self.can_dis<=1:	
			if self.pos==0:
				self.disparo()
			elif self.pos==4:
				i=0
				while i>=3:
					self.hab_1(8,dir_dis[i])
					i+=1
			elif self.pos==2:
				self.hab_1(8,'downright')
				self.hab_1(8,'upleft')
				self.hab_1(8,'downleft')
				self.hab_1(8,'upright')
			elif self.pos==1:
				self.hab_1(8,'downright')
				self.hab_1(8,'upleft')
				self.hab_1(8,'downleft')
				self.hab_1(8,'upright')
				self.hab_1(8,'down')
				self.hab_1(8,'left')
				self.hab_1(8,'up')
				self.hab_1(8,'right')
			self.can_dis+=1
		else:
			if self.delay>=200:
				self.can_dis=0
				self.delay=0
			else:
				self.delay+=1
		self.rect.x += self.vx
		self.rect.y += self.vy


class Disparos(pg.sprite.Sprite):
	cambio_x = 0
	cambio_y = 0

	def __init__(self, game, x, y,paredes,enemigos,dire,chase=False):
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
	    self.chase = chase
	    self.target = game.player
	    self.paredes = paredes
	    self.enemigos = enemigos
	    self.dir = dire

	def d_up(self):
	    self.rect.top -= 3
	def d_down(self):
	    self.rect.bottom += 3
	def d_right(self):
	    self.rect.right += 3
	def d_left(self):
	    self.rect.left -= 3

	def d_up_left(self):
		self.rect.top -=3
		self.rect.left -= 3

	def d_up_right(self):
		self.rect.top -= 3
		self.rect.right += 3

	def d_bottom_left(self):
		self.rect.bottom += 3
		self.rect.left -= 3

	def d_bottom_right(self):
		self.rect.bottom += 3
		self.rect.right += 3

	def movement_wall(self):
		self.vx, self.vy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y 
		dist = math.hypot(self.vx, self.vy)
		if dist == 0:
		    dist = 1
		else:
		    self.vx, self.vy = self.vx / dist, self.vy / dist

	def movement(self):
		if self.dir=='up':
			self.d_up()
		elif self.dir=='upleft':
			self.d_up_left()
		elif self.dir=='upright':
			self.d_up_right()
		elif self.dir=='down':
			self.d_down()
		elif self.dir=='downleft':
			self.d_bottom_left()
		elif self.dir=='downright':
			self.d_bottom_right()
		elif self.dir=='right':
			self.d_right()
		elif self.dir=='left':
			self.d_left()

	def update(self):
		if self.chase:
			self.image = pg.image.load('bala_chaser.png')
			self.damage = 2
			self.movement_wall()
		else:
			self.movement()
		self.rect.x += self.vx * 3
		self.rect.y += self.vy * 3 
		self.colision()

	def colision(self):
	    lista_paredes = pg.sprite.spritecollide(self,self.paredes,False)
	    lista_enemigos = pg.sprite.collide_rect(self,self.game.player)
	    for i in lista_paredes:
	        self.kill()
	    if lista_enemigos:
	    	self.kill()
	    	self.game.player.heal -= self.damage
	    	if self.game.player.heal <= 0:
	    		self.game.player.kill()
