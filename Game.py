import pygame, sys, time
from Wall import Wall
from Player import Player
from Level import Level
from pygame.locals import *

class Game:

	def __init__(self, level_name):
		pygame.init()
		self.screen = pygame.display.set_mode((1,1))
		self.level = Level(level_name)
		self.screen = pygame.display.set_mode((self.level.getX() * 60,self.level.getY() * 80))
		self.color = (0,0,0)
		location = self.level.findPlayer()
		self.rectColor = (100,100,200)
		self.player = Player(location[0] * 60 + 10, (location[1] * 80) + 30)
	
	def run(self):
		output = 0
		while True:
			self.player.tick(self.level)
			self.level.doCollision(self.player)
			output = self.level.tick(self.player) 
			if output != 0:
				break
			self.move()
			self.screen.fill(self.color)
			self.level.render(self.screen)
			self.screen.blit(self.player.draw(),(self.player.getX(), self.player.getY()))
			pygame.draw.rect(self.screen,self.rectColor, (self.player.getX(), self.player.getY(), 40, 50), 1)
			pygame.display.update()
			time.sleep(.03)
		pygame.quit()
		return output

	def move(self):
		for event in pygame.event.get():
        		if event.type == pygame.QUIT:
            	 		pygame.quit() 
				sys.exit()
		keys = pygame.key.get_pressed()
		if keys[K_RIGHT]:
			self.player.image = self.player.image_right
			self.player.moveRight()
			if self.level.willCollide(self.player):
				self.player.moveLeft()
		if keys[K_UP]:
			self.player.up(self.level)

		if keys[K_DOWN]:
			self.player.down(self.level)

		if keys[K_LEFT]:
			self.player.image = self.player.image_left
			self.player.moveLeft()
			if self.level.willCollide(self.player):
				self.player.moveRight()
				


