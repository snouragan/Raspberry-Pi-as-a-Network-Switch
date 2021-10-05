# library to convert the bytes sent from arduino 
# to information about the relay state
# 0 - relay on 
# 1 - relay off
import sys
import curses
from curses import wrapper, textpad

# move cursor: window.move(new y, new x)
# get str from user: window.getstr(y,x,n) 
# get key: window.getke([y,x])

class Relay:
	state = 0b11111111
	numberOfRelays = 8 
	stdscr = curses.initscr()
	SCREEN_WIDTH = curses.COLS
	SCREEN_HEIGHT = curses.LINES
	WIDTH = SCREEN_WIDTH//10
	HEIGHT = SCREEN_HEIGHT//3
	SPACE = (SCREEN_WIDTH - (WIDTH*numberOfRelays)) // (numberOfRelays+1)
	MARGINX = (SCREEN_WIDTH - (numberOfRelays*WIDTH + (numberOfRelays+1)*SPACE)) // 2
	MARGINY = 1

	def __init__(self, number, name="Relay"):
		self.name = name
		self.number = number
		curses.noecho()
		curses.cbreak()
		Relay.stdscr.keypad(True)
		curses.start_color()
		
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN) #ON
		curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) #OFF
		curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_CYAN) #RELAY_FILL
		curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN) #RELAY_WRITING
		curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE) #BORDER

		curses.curs_set(0) # cursor set to invisible
	def __del__(self):
		curses.nocbreak()
		Relay.stdscr.keypad(False) 
		curses.echo()
		curses.endwin()
	def isOn(self):
		return False if Relay.state & 1<< self.number else True 
	def drawRelay(self):
		self.uly = Relay.MARGINY
		self.ulx = Relay.MARGINX + Relay.SPACE*(self.number+1) + self.number*Relay.WIDTH 
		self.lry = Relay.MARGINY + Relay.HEIGHT
		self.lrx = self.ulx + Relay.WIDTH
		Relay.stdscr.attron(curses.color_pair(5))
		curses.textpad.rectangle(Relay.stdscr, self.uly, self.ulx, self.lry, self.lrx)
		Relay.stdscr.attron(curses.color_pair(5))

		Relay.stdscr.attron(curses.color_pair(3))
		for col in range(self.ulx+1, self.lrx):
			for line in range(self.uly+1, self.lry):
				Relay.stdscr.addch(line, col, ' ')
		Relay.stdscr.attroff(curses.color_pair(3))

	def drawName(self):
		length = len(self.name)
		self.NAMEX = self.ulx + ((self.lrx - self.ulx) // 2) - (length//2)
		self.NAMEY = (Relay.HEIGHT // 4) + Relay.MARGINY
		Relay.stdscr.attron(curses.color_pair(4))
		Relay.stdscr.addstr(self.NAMEY, self.NAMEX, self.name)
		Relay.stdscr.attroff(curses.color_pair(4))
	def drawNumber(self):
		self.NUMBERX = self.ulx + ((self.lrx - self.ulx) // 2)
		self.NUMBERY = (Relay.HEIGHT // 2) + Relay.MARGINY
		Relay.stdscr.attron(curses.color_pair(4))
		Relay.stdscr.addstr(self.NUMBERY, self.NUMBERX, str(self.number+1))
		Relay.stdscr.attroff(curses.color_pair(4))
	def drawDetails(self):
		self.drawName()
		self.drawNumber()
	def drawState(self):
		self.STATEY = Relay.HEIGHT*2 + Relay.MARGINY
		if self.isOn():
			state = 'ON '
			self.STATEX = self.ulx + ((self.lrx - self.ulx) // 2) - (len(state)//2)
			Relay.stdscr.attron(curses.color_pair(1))
			Relay.stdscr.addstr(self.STATEY, self.STATEX, state)
			Relay.stdscr.attroff(curses.color_pair(1))
		else:
			state = 'OFF'
			self.STATEX = self.ulx + ((self.lrx - self.ulx) // 2) - (len(state)//2)
			Relay.stdscr.attron(curses.color_pair(2))
			Relay.stdscr.addstr(self.STATEY, self.STATEX, state)
			Relay.stdscr.attroff(curses.color_pair(2))

		Relay.stdscr.attron(curses.color_pair(5))
		curses.textpad.rectangle(Relay.stdscr, self.STATEY-1, self.STATEX-1, self.STATEY+1, self.STATEX+3)
		Relay.stdscr.attroff(curses.color_pair(5))
	def drawCommands(self):
		key = 'F' + str(self.number+1)
		Relay.stdscr.addstr(Relay.HEIGHT*2 + Relay.MARGINY + 3, self.ulx + ((self.lrx - self.ulx) // 2), key)
		Relay.stdscr.addstr(Relay.SCREEN_HEIGHT-1, 1, 'Toggle state on key press')
	def drawByteState(self):
		self.STATEX = (Relay.SCREEN_WIDTH//2) - 6
		self.STATEY = Relay.SCREEN_HEIGHT//2
		Relay.stdscr.addstr(self.STATEY-1, self.STATEX+4, 'BYTE')
		Relay.stdscr.addstr(self.STATEY, self.STATEX, str(bin(Relay.state)))
		Relay.stdscr.addstr(self.STATEY, self.STATEX, '  ')
	def background(self):
		self.drawRelay()
#		Relay.stdscr.attron(curses.A_BOLD)
		self.drawDetails()
#		Relay.stdscr.attroff(curses.A_BOLD)
		self.drawState()
		self.drawCommands()
		self.drawByteState()
		Relay.stdscr.refresh()
	def readKey():
		key = Relay.stdscr.get_wch()
		if key not in range(265, 273):
			return 0
		else:
			return{
				curses.KEY_F1 : 1,
				curses.KEY_F2 : 2,
				curses.KEY_F3 : 3,
				curses.KEY_F4 : 4,
				curses.KEY_F5 : 5,
				curses.KEY_F6 : 6,
				curses.KEY_F7 : 7,
				curses.KEY_F8 : 8,
			       }[key]
	def toggleRelay():
		relayNumber = Relay.readKey()-1
		if relayNumber == -1:
			return
		if Relay.state & (1<<relayNumber) == 0:
			Relay.state += (0b00000001 << relayNumber)
		else:
			Relay.state -= (0b00000001 << relayNumber)
	def updateState(self):
		Relay.updateScreen()
		self.drawState()
		self.drawByteState()
		self.drawCommands()
		return Relay.state
	def updateScreen():
		if curses.is_term_resized(Relay.SCREEN_HEIGHT, Relay.SCREEN_WIDTH):
			newHEIGHT, newWIDTH = dimensions = Relay.stdscr.getmaxyx()
			Relay.SCREEN_WIDTH = newWIDTH
			Relay.SCREEN_HEIGHT = newHEIGHT
			Relay.WIDTH = Relay.SCREEN_WIDTH//10
			Relay.HEIGHT = Relay.SCREEN_HEIGHT//3
			Relay.SPACE = (Relay.SCREEN_WIDTH - (Relay.WIDTH*Relay.numberOfRelays)) // (Relay.numberOfRelays+1)
			Relay.MARGINX = (Relay.SCREEN_WIDTH - (Relay.numberOfRelays*Relay.WIDTH + (Relay.numberOfRelays+1)*Relay.SPACE)) // 2
			Relay.MARGINY = 1
			Relay.stdscr.clear()
			Relay.stdscr.refresh()
			return True
		return False
	def debug(x):
		Relay.stdscr.addstr(0,0,str(bin(x))) 
		Relay.stdscr.refresh()
		pass

if __name__ == '__main__':
	try:
		numberOfRelays = 8
		relays = []
		for _ in range(numberOfRelays):
			relays.append(Relay(_))
		for relay in relays:
			relay.background()
		while True:
			Relay.toggleRelay()
			if Relay.updateScreen():
				for relay in relays:
					relay.background()
			for relay in relays:
				relay.updateState()
	except KeyboardInterrupt:
		curses.nocbreak()
		Relay.stdscr.keypad(False)
		curses.echo()
		curses.endwin()
		print('\nInterrupted')
		sys.exit(0)
	finally:
		curses.nocbreak()
		Relay.stdscr.keypad(False)
		curses.echo()
		curses.endwin()


