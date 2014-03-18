import pygame, os
from pygame.locals import *
class Player:
	
	def __init__(self, x, y):
		self.health = 10
		self.rect = Rect(x, y)
		pygame.init()
		self.upVelocity = 0
		path = os.path.dirname(__file__) + r"\Images\player-right.gif"
		self.image_right = pygame.image.load(path)
		self.image_right.convert()
		path = os.path.dirname(__file__) + r"\Images\player-left.gif"
		self.image_left = pygame.image.load(path)
		self.image_left.convert()
		path = os.path.dirname(__file__) + r"\Images\player-up.gif"
		self.image_up = pygame.image.load(path)
		self.image_up.convert()
		self.image = self.image_right

	def jump(self, level):
		if self.upVelocity == 0 and level.isObjectUnder(self):
			self.upVelocity = 24

	def up(self, level):
		if level.isInLadder(self):
			self.image = self.image_up
			self.moveUp(-3)
			if level.willCollide(self):
				self.moveUp(3)
		else:
			self.jump(level)

	def down(self, level):	
		if level.isInLadder(self):
			self.moveUp(3)
			if level.willCollide(self):
				self.moveUp(-3)

	def moveLeft(self):
		self.rect.moveX(-4)

	def moveRight(self):
		self.rect.moveX(4)
	
	def moveUp(self, distance):
		self.rect.moveY(distance)

	def getX(self):
		return self.rect.getX()

	def getY(self):
		return self.rect.getY()

	def draw(self):
		return self.image
	
	def getBottom(self):
		return self.rect.getBY()

	def isJumping(self):
		return self.upVelocity > 0

	def fall(self):
		self.upVelocity = 0

	def getRight(self):
		return self.rect.getRX()

	def moveX(self, distance):
		self.rect.moveX(distance)

	def moveY(self, distance):
		self.rect.moveY(distance)

	def tick(self, level):

		if self.upVelocity == 0:
			if not level.isObjectUnder(self):
				d = level.distanceObjectUnder(self)
				if d > 8:
					self.rect.moveY(8)
				elif d != 0:
					self.rect.moveY(d - 1)
				elif d ==0 and level.isEmptyUnder(self):
					self.rect.moveY(8)

		if self.upVelocity > 0:
			self.rect.moveY(self.upVelocity * -1)
			self.upVelocity -=3


		if self.upVelocity < 0:
			self.upVelocity = 0

		level.doObjectUnder(self)
		

class Rect:

	def __init__(self, x, y):
		self.leftX = x
		self.rightX = x + 40
		self.topY = y
		self.bottomY = y + 50

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

	def moveX(self, distance):
		self.leftX += distance
		self.rightX += distance

	def moveY(self, distance):
		self.topY += distance
		self.bottomY +=distance
