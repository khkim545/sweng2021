from tetris import *
from random import *

def rotate(m_array):
    size = len(m_array)
    r_array = [[0] * size for _ in range(size)]

    for y in range(size):
        for x in range(size):
            r_array[x][size-1-y] = m_array[y][x]

    return r_array

def initSetOfBlockArrays():
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
    
if __name__ == "__main__":
    setOfBlockArrays = initSetOfBlockArrays()

    Tetris.init(setOfBlockArrays)
    board = Tetris(20, 15)

    idxBlockType = randint(0, 6)
    key = '0' + str(idxBlockType)
    board.accept(key)
    board.printScreen()
      
    while True:
        key = input('Enter a key from [ q (quit), a (left), d (right), s (down), w (rotate), \' \' (drop) ] : ')
        
        if key != 'q':
          state = board.accept(key)
          board.printScreen()
          
          if state == TetrisState.NewBlock:
              idxBlockType = randint(0, 6)
              key = '0' + str(idxBlockType)
              state = board.accept(key)
              if state == TetrisState.Finished:
                  board.printScreen()
                  print('Game Over!!!')
                  break
              board.printScreen()
        else:
          print('Game aborted...')
          break
    
    print('Program terminated...')

### end of pytet.py
