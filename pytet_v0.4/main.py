from tetris import *
from random import *

import os
import sys
import tty
import termios
import signal

def clearScreen(numlines=100):
	if os.name == 'posix':
		os.system('clear')
	elif os.name in ['nt', 'dos', 'ce']:
		os.system('CLS')
	else:
		print('\n' * numlines)
	return

def printScreen(board):
	clearScreen()
	array = board.oScreen.get_array()

	for y in range(board.oScreen.get_dy()-Tetris.iScreenDw):
		line = ''
		for x in range(Tetris.iScreenDw, board.oScreen.get_dx()-Tetris.iScreenDw):
			if array[y][x] == 0:
				line += '□'
			elif array[y][x] == 1:
				line += '■'
			else:
				line += 'XX'
		print(line)

	print()
	return

def unregisterAlarm():
	signal.alarm(0)
	return

def registerAlarm(handler, seconds):
	unregisterAlarm()
	signal.signal(signal.SIGALRM, handler)
	signal.alarm(seconds)
	return

def timeout_handler(signum, frame): 
	#print("timeout!")
	raise RuntimeError ### we have to raise error to wake up any blocking function
	return

def getChar():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch
 
def readKey():
	c1 = getChar()
	if ord(c1) != 0x1b: ### ESC character
		return c1
	c2 = getChar()
	if ord(c2) != 0x5b: ### '[' character
		return c1
	c3 = getChar()
	return chr(0x10 + ord(c3) - 65)

def readKeyWithTimeOut():
	registerAlarm(timeout_handler, 1)
	try:
		key = readKey()
		return key
	except RuntimeError as e:
		pass # print('readkey() interrupted!')

	return
 
def rotate(m_array):
    size = len(m_array)
    r_array = [[0] * size for _ in range(size)]

    for y in range(size):
        for x in range(size):
            r_array[x][size-1-y] = m_array[y][x]

    return r_array

def initSetOfBlockArrays():
    global nBlocks

    arrayBlks = [ [ [ 0, 0, 1, 0 ],     # I shape
                    [ 0, 0, 1, 0 ],     
                    [ 0, 0, 1, 0 ],     
                    [ 0, 0, 1, 0 ] ],   
                  [ [1, 0, 0],          # J shape
                    [1, 1, 1],          
                    [0, 0, 0] ],
                  [ [0, 0, 1],          # L shape
                    [1, 1, 1],          
                    [0, 0, 0] ],        
                  [ [1, 1],             # O shape
                    [1, 1] ],           
                  [ [0, 1, 1],          # S shape
                    [1, 1, 0],          
                    [0, 0, 0] ],
                  [ [0, 1, 0],          # T shape    
                    [1, 1, 1],          
                    [0, 0, 0] ],
                  [ [1, 1, 0],          # Z shape
                    [0, 1, 1],          
                    [0, 0, 0] ]         
                ]

    nBlocks = len(arrayBlks)
    setOfBlockArrays = [[0] * 4 for _ in range(nBlocks)]

    for idxBlockType in range(nBlocks):
        temp_array = arrayBlks[idxBlockType]
        setOfBlockArrays[idxBlockType][0] = temp_array
        for idxBlockDegree in range(1,4):
            temp_array = rotate(temp_array)
            setOfBlockArrays[idxBlockType][idxBlockDegree] = temp_array

    return setOfBlockArrays
    
def processKey(board, key):
	global nBlocks 

	state = board.accept(key)
	printScreen(board)
          
	if state != TetrisState.NewBlock:
		return state

	idxBlockType = randint(0, nBlocks-1)
	key = '0' + str(idxBlockType)
	state = board.accept(key)
	printScreen(board)

	if state != TetrisState.Finished:
		return state

	return state

if __name__ == "__main__":
	setOfBlockArrays = initSetOfBlockArrays()

	Tetris.init(setOfBlockArrays)
	board = Tetris(20, 15)

	idxBlockType = randint(0, nBlocks-1)
	key = '0' + str(idxBlockType)
	state = board.accept(key)
	printScreen(board)

	while True:
		key = readKeyWithTimeOut()
		if not key:
			key = 's'
		#print(repr(key))
        
		if key == 'q':
			state = TetrisState.Finished
			print('Game aborted...')
			break

		state = processKey(board, key)
		if state == TetrisState.Finished:
			print('Game Over!!!')
			break
    
	unregisterAlarm()
	print('Program terminated...')

### end of main.py


