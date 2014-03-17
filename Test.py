import pygame, sys, time
from Wall import Wall
from Player import Player
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,600))
player = Player(70, 90)
walls = [Wall(0,0), Wall(1,0), Wall(2,0), Wall(0,1), Wall(3,0), Wall(0,2)]
color = (0,0,0)
screen.fill(color)

while (True):
	screen.fill(color)
	keys = pygame.key.get_pressed()
	if keys[K_RIGHT]:
		player.moveRight()
	if keys[K_LEFT]:
		player.moveLeft()
	screen.blit(player.draw(), (player.getX(), player.getY()))
	for wall in walls:
		screen.blit(wall.draw(), (60 * wall.getX(),80 * wall.getY()))
	pygame.display.update()
	for event in pygame.event.get():
        	if event.type == pygame.QUIT:
            	 	pygame.quit(); sys.exit();
	time.sleep(.03)
