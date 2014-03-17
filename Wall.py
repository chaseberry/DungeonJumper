import pygame, os
from pygame.locals import *
class Wall:

	def __init__(self, x, y):
		pygame.init()
		self.x_location = x
		self.y_location = y
		self.rect = Rect(x, y)
		path = os.path.dirname(__file__) + "\Images\Wall.gif"
		self.image = pygame.image.load(path)
		self.image.convert()

	def draw(self):
		return self.image

	def getX(self):
		return self.rect.getX()

	def getY(self):
		return self.rect.getY()

	def getRX(self):
		return self.rect.getRX()

	def pullPlayer(self, player):
		pass

	def pushPlayer(self, player):
		if self.rect.getBY() >= player.getY():
			player.moveY(self.rect.getBY() - player.getY() + 1)
			player.fall()

	def contains(self, x, y):
		return self.rect.contains(x, y)

	def collide(self, player):
		return not(player.getY() >= self.rect.getBY() or player.getBottom() <= self.rect.getY() or player.getX() >= self.rect.getRX() or player.getRight() <= self.rect.getX())

	def toString(self):
		return '1'

class Rect:

	def __init__(self, x, y):
		self.leftX = x * 60
		self.rightX = (x + 1) * 60
		self.topY = y * 80
		self.bottomY = (y + 1) * 80

	def contains(self, x, y):
		return self.leftX < x < self.rightX and self.topY < y < self.bottomY 

	def getX(self):
		return self.leftX
	
	def getY(self):
		return self.topY

	def getRX(self):
		return self.rightX

	def getBY(self):
		return self.bottomY
