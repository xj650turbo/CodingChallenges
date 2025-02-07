import numpy as np

class Moves():
    # the default mask allows to move only left, right, up, and down from center (current position)
    def __init__(self, searchMask = [ 
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
            ]):
        # moves are defined based based on a 3x3 array
        # Legal moves are indicated by ones (the center is the current position where a move starts)
        # must be in this order, searchMask is processes row wise from top to bottom, left to right at each row
        self.directions = ['^', '<', '>', 'v']   
        self.moveCommands = {}
        self.moves = []
        self.setMoves(searchMask)

    
    def move(self, moveCmd, pos):
        return pos + self.moveCommands[moveCmd]

    # get moves based on a 3x3 array. legal moves are indicated by ones, center is current position
    def getMoves(self, searchMask):
        searchMask = np.array(searchMask, dtype=np.int32)
        indices = np.where(searchMask == 1)
        indexTuples = list(zip(indices[0], indices[1]))
        # transform from x,y indices to all possible moves
        moves = np.array([[(el - 1) for el in nestedList] for nestedList in indexTuples])
        return moves   


    def getPerpendicularMoves(self, move):
        p1 = np.array([-move[1], move[0]], dtype=np.int32)
        p2 = np.array([move[1], -move[0]], dtype=np.int32)
        return p1, p2


    # set a search mask on how a map can be walked. For example:
    # (default) left/right/up/down | diagonally/l/r/u/d: | diagonally only:
    # [[0, 1, 0],                  |  [[1, 1, 1],        |  [[1, 0, 1], 
    #  [1, 0, 1],                  |   [1, 0, 1],        |   [0, 0, 0],
    #  [0, 1, 0]]                  |   [1, 1, 1]]        |   [1, 0, 1]]
    def setMoves(self, searchMask):
        self.moves = self.getMoves(searchMask)
        self.moveCommands.update(zip(self.directions, self.getMoves(searchMask)))


    # supports multiples on 90 degrees: 90, 180, 270, 360
    def turn(self, dir, angle):
        currMove = self.moveCommands[dir]
        theta = (angle/180.) * np.pi
        rotMatrix = np.eye(2)    
        rotMatrix[0][0] = rotMatrix[1][1] = np.cos(theta)
        rotMatrix[1][0] = np.sin(theta) 
        rotMatrix[0][1] = -rotMatrix[1][0] 

        move = np.dot(currMove, rotMatrix).astype(int)
        newDir = [key for key, val in self.moveCommands.items() if np.all(val == move)]

        return (newDir[0], move)

