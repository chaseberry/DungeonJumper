from Game import Game
from Editor import Editor
import os, random


def game_looper(level):
	game = Game(level)
	result  = 0
	while not result == -5:
		result = game.run()
		again = 'n'
		if result == -1:
			print 'You were crushed'
			again = raw_input('Try again? (Y/N): ')
		elif result == -2:
			print 'You fell to your death'
			again = raw_input('Try again? (Y/N): ')
		else:
			print 'You escaped that room!'
			again = result
		if again:
			if again[0] == 'N' or again[0] == 'n':
				break
			elif again[0] == 'Y' or again[0] == 'y':
				game = Game(level)
			elif result != -1 and result !=-2:
				game = Game(again)
			else:
				break
		else:
			break



result = 0

print 'Welcome to Dungeon Jumper!'
while True:
	line = raw_input('say a level name or help for more: ')
	if line:
		if line[0] == 'h':
			print 'Simply type a levels name to play it'
			print 'quit to quit the game'
			print 'or type edit with the edit commands to pull up the editor'
			print 'edit has two modes, load and new'
			print 'edit load level_name'
			print 'edit new x_value y_value level_name'
		elif line[0:4] == 'edit':
			data = line.replace('editor','').replace('edit','').split()
			editor = Editor(data)
		elif line[0] == 'q' or line[0] == 'Q':
			break
		else:
			path = os.path.abspath(os.path.dirname(__file__) + "\Levels\\")
			if line[0] == 'r' or line[0] == 'R':
				game_looper(random.choice(os.listdir(path)))
			else:
				if os.path.isfile(path + '\\' +line):
					game_looper(line)
				else:
					print 'Level not found'

	
	
