import os, math
from Wall import Wall
from Ladder import Ladder
from Platform import Platform
from Door import Door

class Level:

	def __init__(self, name):
		path = os.path.abspath(os.path.dirname(__file__) + r"\Levels\\" + name)
		file = open(path)
		line = file.readline()
		line = line.split(",")
		self.x = int(line[0])
		self.y = int(line[1])
		self.level = [[0 for x in range(self.y)] for x in range(self.x)]
		cur_line = 0
		line = file.readline()
		while line is not '':
			data = line.split(",")
			for z in range(len(data)):
				self.level[z][cur_line] = self.getItem(int(data[z]), z, cur_line)
			cur_line+=1
			line = file.readline()
	
	def getItem(self, item_id, x, y):
		if item_id == -1:
			return -1
		elif item_id == 0:
			return 0
		elif item_id == 1:
			return Wall(x, y)
		elif item_id == 2:
			return Door(x, y)
		elif item_id == 3:
			return Ladder(x, y)
			
		elif item_id > 4:
			data = str(item_id)#0 --> up, 1--> down 2-->left 3-->right
			return Platform(x, y, int(data[1]), int(data[2]))

	def findPlayer(self):
		for z in range(self.x):
			for v in range(self.y):
				if self.level[z][v] == -1:
					self.level[z][v] = 0
					return (z,v)


	def getX(self):
		return self.x

	def getY(self):
		return self.y
	
	def willCollide(self, player):
		for z in range(self.x):
			for v in range(self.y):
				if self.level[z][v] != 0:
					if self.level[z][v].collide(player):
						return True
		return False

	def tick(self, player):
		if self.isInDoor(player):
			return 1

		if self.willCollide(player):
			return -1
		elif player.getBottom() >= (80 * self.y):
			return -2

		for z in range(self.x):
			for v in range(self.y):
				if isinstance(self.level[z][v], Platform):
					self.level[z][v].tick(player)
		return 0

	def doObjectUnder(self, player):
		y = player.getBottom() + 3
		x = (player.getX() + player.getRight()) / 2
		for z in range(self.x):
			for v in range(self.y):
				if self.level[z][v] != 0:
					if self.level[z][v].contains(x, y) and isinstance(self.level[z][v], Platform):
						self.level[z][v].pushPlayer(player)
						if self.willCollide(player):
							self.level[z][v].pullPlayer(player)

	def isInDoor(self, player):
		y = player.getBottom() - 3
		x = player.getX()
		rx = player.getRight()
		for z in range(self.x):
			for v in range(self.y):
				if isinstance(self.level[z][v], Door):
					if self.level[z][v].contains(x, y) or self.level[z][v].contains(rx, y):
						return True
		return False

	def isInLadder(self, player):
		y = player.getBottom() - 3
		x = player.getX()
		rx = player.getRight()
		for z in range(self.x):
			for v in range(self.y):
				if isinstance(self.level[z][v], Ladder):
					if self.level[z][v].contains(x, y) or self.level[z][v].contains(rx, y):
						return True
		return False
		

	def distanceObjectUnder(self, player):
		maxD = 99999999
		y = player.getBottom()
		x = player.getX()
		rx = player.getRight()
		for z in range(self.x):
			for v in range(self.y):
				if self.level[z][v] != 0 and not isinstance(self.level[z][v], Ladder) and self.level[z][v].getY() > y:
					if self.level[z][v].getX() < x < self.level[z][v].getRX() or self.level[z][v].getRX() > rx > self.level[z][v].getX():
						maxD = min(maxD, self.level[z][v].getY() - y)
		return 0 if maxD == 99999999 else maxD


	def isEmptyUnder(self, player):#re-write to use y-values, not y co-ords
		yBot = player.getBottom()
		y = int(math.floor((player.getBottom()) / 80))
		x = int(math.floor((player.getX()) / 60))
		rx = int(math.floor((player.getRight()) / 60))
		if y+1 >= len(self.level[x]):
			return True
		if x == rx and self.level[x][y + 1] == 0:
			return True
		elif self.level[x][y+1] == 0 and self.level[rx][y] == 0:
			return True
		return False

	def isObjectUnder(self, player):
		y = player.getBottom() + 3
		x = player.getX()
		rx = player.getRight()
		for z in range(self.x):
			for v in range(self.y):
				if self.level[z][v] != 0 and not isinstance(self.level[z][v], Door):
					if self.level[z][v].contains(x, y) or self.level[z][v].contains(rx, y):
						return True
		return False

	def doCollision(self, player):
		object = -1
		for z in range(self.x):
			for v in range(self.y):
				if self.level[z][v] != 0:
					if self.level[z][v].collide(player):
						object = self.level[z][v]
		if object != -1:
			object.pushPlayer(player)

	def render(self, screen):
		for z in range(self.x):
			for v in range(self.y):
				if(self.level[z][v] is not 0):
					element = self.level[z][v]
					screen.blit(element.draw(),(element.getX(),element.getY()))
		

