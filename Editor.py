import pygame, time, math
import os
from pygame.locals import *
from Wall import Wall
from Ladder import Ladder
from Platform import Platform
from Door import Door
class Editor:

	def __init__(self, argv):
		pygame.init()
		if argv[0] == 'new':
			self.x = int(argv[1])
			self.y = int(argv[2])
			self.file_name = os.path.abspath(os.path.dirname(__file__) + r"\Levels\\" + argv[3])
			self.screen = pygame.display.set_mode((self.x * 60, self.y * 80))
			self.level = [[0 for z in range(self.y)] for v in range(self.x)]
		
		else:
			self.create(argv[1])
		
		self.block = 1
		self.allowedClick = True
		self.color = (0, 0, 0)
		self.draw()
		self.tiles = [Wall(0,0), Platform(1,0,0,0), Door(2,0), Ladder(3,0)]
		while True:
			self.getMouse()
			time.sleep(.1)


	def create(self, fileName):
		path = os.path.abspath(os.path.dirname(__file__) + r"\Levels\\" + fileName) # must be changed later
		file = open(path)
		self.file_name = path
		line = file.readline()
		line = line.split(",")
		self.x = int(line[0])
		self.y = int(line[1])
		self.mode = True
		self.screen = pygame.display.set_mode((self.x * 60, self.y * 80))
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

	def draw(self):
		if self.mode:
			self.screen.fill(self.color)	
			for z in range(self.x):
				for v in range(self.y):
					if(self.level[z][v] is not 0 and self.level[z][v] is not -1):
						element = self.level[z][v]
						self.screen.blit(element.draw(),(element.getX(),element.getY()))
					if(self.level[z][v] == -1):
						pygame.draw.rect(self.screen, (0, 0, 255), (z * 60, v * 80, 60, 80))
			for z in range(self.x):
				for v in range(self.y):
					pygame.draw.rect(self.screen, (255, 255, 225), (z * 60, v * 80, 60, 80), 1)
		else:
			self.screen.fill(self.color)
			for z in range(len(self.tiles)):
				element = self.tiles[z]
				self.screen.blit(element.draw(),(element.getX(),element.getY()))
			pygame.draw.rect(self.screen, (0, 0, 255), (5 * 60, 0, 60, 80))

		pygame.display.update()

	def getMouse(self):
		pygame.event.get()
		keys = pygame.key.get_pressed()
		if keys[K_0]:
			self.block = 0
		elif keys[K_1]:
			self.block = 1
		elif keys[K_3]:
			self.block = 3
		elif keys[K_2]:
			self.block = 2
		elif keys[K_4]:
			self.block = 4
		elif keys[K_s]:
			 self.getSave()
			 pygame.quit()
		elif keys[K_p]:
			self.block = -1
		mouse = pygame.mouse.get_pressed()

		if not mouse[0] and not mouse[2]:
			self.allowedClick = True

		if mouse[0] and self.allowedClick:
			self.click()	
			self.allowedClick = False
	

		if mouse[2]:
			self.mode = not self.mode
			self.allowedClick = False
			self.draw()

	def getSave(self):
		string = str(self.x) + ',' + str(self.y) + '\n'
		for v in range(self.y):
			for z in range(self.x):
				string += str(self.level[z][v]) if self.level[z][v] == 0 or self.level[z][v] == -1 else self.level[z][v].toString()
				if z < (self.x - 1):
					string += ','
			string += '\n'
		file = open(self.file_name, 'w')
		file.write(string)

	def click(self):
		if self.mode:
			points = pygame.mouse.get_pos()
			x = int(math.floor(points[0] / 60))
			y = int(math.floor(points[1] / 80))
			if self.block == 0:
				self.level[x][y] = 0
			elif self.block == 1:
				self.level[x][y] = Wall(x, y)
			elif self.block == 2:
				for z in range(self.x):
					for v in range(self.y):
						if isinstance(self.level[z][v], Door):
							self.level[z][v] = 0
				self.level[x][y] = Door(x, y)
			elif self.block == -1:
				for z in range(self.x):
					for v in range(self.y):
						if self.level[z][v] == -1:
							self.level[z][v] = 0
				self.level[x][y] = -1
			elif self.block == 3:
				self.level[x][y] = Ladder(x, y)
			elif self.block == 4:
				self.block = 5
				self.start = (x, y)
			elif self.block == 5:
				if not(self.start[0] != x and self.start[1] != y):
					if self.start[0] == x:
						orientation = 0 if y < self.start[1] else 1
						distance = abs(y - self.start[1])
					else:
						orientation = 2 if x < self.start[0] else 3
						distance = abs(x - self.start[0])
					self.block = 4
					self.level[self.start[0]][self.start[1]] = Platform(self.start[0], self.start[1], orientation, distance)
		else:
			points = pygame.mouse.get_pos()
			x = int(math.floor(points[0] / 60))
			y = int(math.floor(points[1] / 80))
			self.mode = True
			if x == 0:
				self.block = 1
			elif x == 1:
				self.block = 4
			elif x == 2:
				self.block = 2
			elif x == 3:
				self.block = 3
			elif x == 4:
				self.block = 0
			elif x == 5:
				self.block = -1
		self.draw()


