import pygame as pg
from settings import *
import time
import math
import random

DIRECCIONES = ['UP','DOWN','RIGHT','LEFT']
dir_dis = ['down','right','left']
dir_dig = ['downleft','downright']

class Boss(pg.sprite.Sprite):
	def __init__(self, game, x, y):
	    self.groups = game.all_sprites
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = pg.Surface((128, 128))
	    self.image.fill(LIGHTGREY)
	    self.rect = self.image.get_rect()
	    self.vx, self.vy = 0, 0
	    self.heal = 200
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
		disparo = Bullet_chase(self.game,self.rect.x,self.rect.y,self.game.walls)
		self.game.lista_disparos.add(disparo)
		disparo = Bullet_chase(self.game,self.rect.x+96,self.rect.y,self.game.walls)
		self.game.lista_disparos.add(disparo)

	def chaser(self):
		disp = chase(self.game,self.rect.x+64,self.rect.y+64,self.game.walls)
		self.game.lista_disparos.add(disp)
		disp = chase(self.game,self.rect.x+64,self.rect.y+64,self.game.walls)
		self.game.lista_disparos.add(disp)
		disp = chase(self.game,self.rect.x+64,self.rect.y+64,self.game.walls)
		self.game.lista_disparos.add(disp)

	def hab_1(self,cant,dire):
		j=0
		pos_y = 0
		while j<=cant:
			i=0
			pos_x=0
			while i<=cant:
				i+=1
				disparo = Disparos(self.game, self.rect.x+pos_x, self.rect.y+pos_y, self.game.walls,self.lista_player,dire)
				if self.heal <= 100:
					disparo.speed = 2
				elif self.heal <= 50:
					disparo.speed = 4
				elif self.heal <= 10:
					disparo.speed = 6
				self.game.lista_disparos.add(disparo)
				pos_x+=16
			j+=1
			pos_y+=16
		
	def update(self):
		print(self.heal)
		self.pos =random.randint(0,2)
		if self.can_dis<=0:	
			if self.pos==0:
				self.chaser()
			elif self.pos==1:
				i=0
				while i<=2:
					self.hab_1(8,dir_dis[i])
					i+=1
				if self.heal <= 100:
					i=0
					while i<=1:
						j=dir_dis[0]+""+dir_dis[1+i]
						self.hab_1(8,j)
						i+=1
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

	def __init__(self, game, x, y,paredes,enemigos,dire):
	    self.groups = game.all_sprites
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = pg.image.load('bala.png')
	    self.rect = self.image.get_rect()
	    self.damage = 1
	    self.speed = 1
	    self.rect.y = y
	    self.rect.x = x
	    self.target = game.player
	    self.paredes = paredes
	    self.enemigos = enemigos
	    self.dir = dire

	def d_down(self):
	    self.rect.bottom += 3 * self.speed
	def d_right(self):
	    self.rect.right += 3 * self.speed
	def d_left(self):
	    self.rect.left -= 3 * self.speed


	def d_bottom_left(self):
		self.rect.bottom += 3 * self.speed
		self.rect.left -= 3 * self.speed

	def d_bottom_right(self):
		self.rect.bottom += 3 * self.speed
		self.rect.right += 3 * self.speed

	def movement(self):
		if self.dir=='down':
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
		self.movement()
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

class Bullet_chase(pg.sprite.Sprite):
	def __init__(self, game, x, y,paredes):
	    self.groups = game.all_sprites, game.lista_enemigos
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = pg.image.load('bala_chaser.png')
	    self.rect = self.image.get_rect()
	    self.damage = 2.5
	    self.heal = 3
	    self.vx, self.vy = 0,0
	    self.rect.y = y
	    self.rect.x = x
	    self.target = game.player
	    self.paredes = paredes

	def movement(self):
		self.vx, self.vy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y 
		dist = math.hypot(self.vx, self.vy)
		if dist == 0:
		    dist = 1
		else:
		    self.vx, self.vy = self.vx / dist, self.vy / dist

	def update(self):
		if self.heal <= 0:
			self.kill()
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

class chase(pg.sprite.Sprite):
	def __init__(self, game, x, y,paredes):
	    self.groups = game.all_sprites
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = pg.image.load('bala.png')
	    self.rect = self.image.get_rect()
	    self.damage = 1.5
	    self.vx, self.vy = 0,0
	    self.rect.y = y
	    self.rect.x = x
	    self.i = 0
	    self.speed = 5
	    self.target = game.player
	    self.paredes = paredes

	def movement(self):
		if self.i==0:
			self.vx, self.vy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y 
			dist = math.hypot(self.vx, self.vy)
			self.i=1
			if dist == 0:
			    dist = 1
			else:
			    self.vx, self.vy = self.vx / dist, self.vy / dist

	def update(self):
		self.movement()
		self.rect.x += self.vx * self.speed
		self.rect.y += self.vy * self.speed
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