import pygame as pg
import random

BASE = 16
ALTURA = 16

class Cuarto (pg.sprite.Sprite):
	def __init__(self,x,y,base,altura):
		self.image = pg.Surface((base,altura))
		self.image.fill((255,0,0))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.x0 = x
		self.base = base
		self.altura = altura

class Puerta(pg.sprite.Sprite):
	def __init__(self,x,y):
		self.image = pg.Surface((BASE,ALTURA))
		self.image.fill((0,255,0))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		

def generar_puerta(cuarto):
	# Why god why
	x0Coord = cuarto.x0 if cuarto.x0 > 0 else 0
	x0CoordBase = cuarto.base if cuarto.base > 0 else 0
	maxCoordX = x0Coord+x0CoordBase
	x = random.randint(x0Coord, maxCoordX)
	puerta = Puerta(x,cuarto.rect.y)
	return puerta

def helperCreate():
	x = random.randint(0,300)
	y = random.randint(0,300)
	base = random.randint(64,256)
	altura = random.randint(64,256)
	cuarto = Cuarto(x,y,base,altura)
	puerta = generar_puerta(cuarto)	
	return cuarto, puerta


def draw(cuarto, puerta):
	pantalla.blit(cuarto.image,(cuarto.rect.x,cuarto.rect.y))
	pantalla.blit(puerta.image,(puerta.rect.x,puerta.rect.y))


def check_colisiona(c,cq):
	cuarto = c
	cuarto_a = cq
	a = pg.sprite.collide_rect(cuarto,cuarto_a)
	return a 


def no_colisiona_con_nadie_de(lista_de_cuartos,cuarto_que_quiero_crear):
	for cuarto_a_comparar in lista_de_cuartos:
		if check_colisiona(cuarto_a_comparar,cuarto_que_quiero_crear):
			return False
		return True
	return True  

pg.init()
pantalla = pg.display.set_mode((400, 400))
pg.display.set_caption("Mapa Aleatorio")
pantalla.fill((255,255,255))
miCuartito , miPuertita = helperCreate()
draw(miCuartito, miPuertita)
cuartos = [miCuartito]
cantidad_de_cuartos_que_quiero_crear = 2

for elem in [cantidad_de_cuartos_que_quiero_crear]:
	cuarto_que_quiero_crear , puerta_que_quiero_crear = helperCreate()
	if no_colisiona_con_nadie_de(cuartos, cuarto_que_quiero_crear):
		draw(cuarto_que_quiero_crear, puerta_que_quiero_crear)

pg.display.flip()
for event in pg.event.get():
    if event.type == pg.QUIT:
        self.quit()