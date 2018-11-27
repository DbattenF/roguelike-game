import pygame as pg
from settings import *
from sprites import *
import time
import math
import random

DIRECCIONES = ['UP','DOWN','RIGHT','LEFT']
dir_dis = ['up','down','right','left']
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
	    self.maxheal = 200
	    self.rect.x = x * TILESIZE
	    self.rect.y = y * TILESIZE
	    self.pos = ''
	    self.can_dis = 0
	    self.damage = 2.5
	    self.delay = 0
	    self.port = 0
	    self.i = 0
	    self.lista_player = pg.sprite.Group()
	    self.lista_player.add(self.game.player)

	def draw_health(self):
		if self.i==0:
			self.backlifebar = BackLifebar(self.game,self.rect.x-32,self.rect.y-32,self.maxheal+4)
			self.lifebar = Lifebar(self.game,self.rect.x-30,self.rect.y-30,self.heal,self.maxheal, self.game.player.damage)
			self.i=1

	def disparo(self):
		disparo = Bullet_chase(self.game,self.rect.x,self.rect.y,self.game.walls)
		self.game.cuarto_actual.list_enemis.add(disparo)
		disparo = Bullet_chase(self.game,self.rect.x+96,self.rect.y,self.game.walls)
		self.game.cuarto_actual.list_enemis.add(disparo)

	def chaser(self):
		disp = chase(self.game,self.rect.x+64,self.rect.y+64,self.game.walls)
		self.game.cuarto_actual.list_enemis_disp.add(disp)
		disp = chase(self.game,self.rect.x+64,self.rect.y+64,self.game.walls)
		self.game.cuarto_actual.list_enemis_disp.add(disp)
		disp = chase(self.game,self.rect.x+64,self.rect.y+64,self.game.walls)
		self.game.cuarto_actual.list_enemis_disp.add(disp)

	def invocacion(self):
		self.invo = portal(self.game,self.rect.x-288,self.rect.y-192)
		self.game.cuarto_actual.list_enemis.add(self.invo)

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
					disparo.speed = 1
				elif self.heal <= 50:
					disparo.speed = 3
				elif self.heal <= 10:
					disparo.speed = 4
				self.game.cuarto_actual.list_enemis_disp.add(disparo)
				pos_x+=16
			j+=1
			pos_y+=16
		
	def update(self):
		self.draw_health()
		self.pos = random.randint(0,3)
		if self.can_dis<=0:	
			if self.pos==0:
				if self.port <=0:
					self.invocacion()
					self.port=1
				elif self.invo.heal==0:
					self.port=0
			
			elif self.pos==1:
				self.disparo()

			elif self.pos==2:
				self.chaser()

			elif self.pos==3:
				i=0
				while i<=3:
					self.hab_1(8,dir_dis[i])
					i+=1
				if self.heal <= 100:
					i=0
					while i<=1:
						j=dir_dis[0]+""+dir_dis[2+i]
						self.hab_1(8,j)
						j=dir_dis[1]+""+dir_dis[2+i]
						self.hab_1(8,j)
						i+=1
			
			self.can_dis+=1
		else:
			if self.delay>=75:
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
	    self.image = IMG_BALA
	    self.rect = self.image.get_rect()
	    self.damage = 1
	    self.speed = 1
	    self.rect.y = y
	    self.rect.x = x
	    self.target = game.player
	    self.paredes = paredes
	    self.enemigos = enemigos
	    self.dir = dire
	    self.colision = True

	def d_up(self):
	    self.rect.top -= 3 * self.speed
	def d_down(self):
	    self.rect.bottom += 3 * self.speed
	def d_right(self):
	    self.rect.right += 3 * self.speed
	def d_left(self):
	    self.rect.left -= 3 * self.speed

	def d_top_left(self):
		self.rect.top -= 3 * self.speed
		self.rect.left -= 3 * self.speed

	def d_top_right(self):
		self.rect.top -= 3 * self.speed
		self.rect.right += 3 * self.speed

	def d_bottom_left(self):
		self.rect.bottom += 3 * self.speed
		self.rect.left -= 3 * self.speed

	def d_bottom_right(self):
		self.rect.bottom += 3 * self.speed
		self.rect.right += 3 * self.speed

	def movement(self):
		if self.dir=='up':
			self.d_up()
		elif self.dir=='upleft':
			self.d_top_left()
		elif self.dir=='upright':
			self.d_top_right()
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
		self.colisione()

	def colisione(self):

		lista_paredes = pg.sprite.spritecollide(self,self.game.cuarto_actual.list_wall,False)
		lista_door = pg.sprite.spritecollide(self,self.game.cuarto_actual.list_door,False)

		for i in lista_paredes:
		    self.kill()

		for i in lista_door:
			self.kill()

class Bullet_chase(pg.sprite.Sprite):
	def __init__(self, game, x, y,paredes):
	    self.groups = game.all_sprites
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = IMG_BALA_CHASER
	    self.rect = self.image.get_rect()
	    self.damage = 1.5
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
		self.drop()
		if self.heal <= 0:
			self.kill()
		self.movement()
		self.rect.x += self.vx * 3
		self.rect.y += self.vy * 3 
		self.colision()

	def drop(self):
		pass

	def colision(self):
		lista_paredes = pg.sprite.spritecollide(self,self.game.cuarto_actual.list_wall,False)
		lista_enemigos = pg.sprite.collide_rect(self,self.game.player)
		lista_door = pg.sprite.spritecollide(self,self.game.cuarto_actual.list_door,False)
		for i in lista_door:
			self.kill()
		for i in lista_paredes:
			self.kill()

class chase(pg.sprite.Sprite):
	def __init__(self, game, x, y,paredes):
	    self.groups = game.all_sprites, game.disparos_enemigos
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = IMG_BALA
	    self.rect = self.image.get_rect()
	    self.damage = 1
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
		lista_door = pg.sprite.spritecollide(self,self.game.door,False)
		for i in lista_door:
			self.kill()

		for i in lista_paredes:
			self.kill()

class portal(pg.sprite.Sprite):
	def __init__(self, game, x, y):
	    self.groups = game.all_sprites, game.portals, game.lista_enemigos
	    pg.sprite.Sprite.__init__(self, self.groups)
	    self.game = game
	    self.image = pg.Surface((TILESIZE,TILESIZE))
	    self.image.fill(WHITE)
	    self.rect = self.image.get_rect()
	    self.rect.x = x
	    self.rect.y = y
	    self.heal = 4
	    self.i = True

	def drop(self):
		pass

	def update(self):
		self.drop()
		if self.i:
			self.enemy = Chaser(self.game,self.rect.x/32,self.rect.y/32,self.game.player)
			self.game.cuarto_actual.list_enemis.add(self.enemy)
			self.i = False
			self.colision_time = pg.time.get_ticks()
		else:
			if pg.time.get_ticks() - self.colision_time > 3500:
				self.i = True
		if self.enemy.heal>=0:
			if self.game.jefes.heal<=200:
				self.game.jefes.heal+=0.02

class Lifebar(pg.sprite.Sprite):
	def __init__(self, game, x, y, maxhp, hp, damage):
		self.groups = game.cuarto_actual.list_lifebar
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((hp, 32))
		self.image.fill(BLACKRED)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.maxhp = hp
		self.boss = game.cuarto_actual.list_boss

	def update(self):
		for i in self.boss:
			self.image = pg.Surface((i.heal,32))
		self.image.fill(BLACKRED)

class BackLifebar(pg.sprite.Sprite):
	def __init__(self, game, x, y,hp):
		self.groups = game.cuarto_actual.list_lifebar
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((hp, 37))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		