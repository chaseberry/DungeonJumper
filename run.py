from Game import Game
from Editor import Editor

def play():
	print 'Got a level you want to play? Type it in'
	print 'Or give me none for a random level that I know'
	level = raw_input('level: ')
	if level == 'none':
		pass
	return level


result = 0

print 'Welcome to Dungeon Jumper!'

while True:
	if result == 0:
		level = play()
	else:
		again = raw_input('Try again? (Y/N)')
		if again == 'N':
			level = play()
	
	if 'editor' in level:
		level = level.replace('editor','').split()
		editor = Editor(level)
	else:
		game = Game(level)
		result = game.run()
		if result == 1:
			result = 0
			print 'You made it out! Congrats'
		elif result == -1:
			print 'You were crushed.'
		elif result == -2:
			print 'You fell to your death'
	
	
