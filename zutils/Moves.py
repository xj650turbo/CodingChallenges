import numpy as np
from itertools import combinations_with_replacement


class Moves():
    # the default mask allows to move only left, right, up, and down from center (current position)
    # moves are defined based based on a 3x3 array
    # Legal moves are indicated by ones (the center is the current position where a move starts)
    def __init__(self, allowed = [ 
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
            ]):
        # All possible directions: they will be filtered based on allowed moves after calling setMoves() 
        self.allPossibleDirections = np.array([
            ['↖', '^', '↗'], 
            ['<', 'x', '>'], 
            ['↙', 'v', '↘']])
        self.allowed = None
        self.directions = []   
        self.moveCommands = {}
        self.moves = []
        self.setMoves(allowed)

    
    def move(self, moveCmd, pos):
        return tuple(pos + self.moveCommands[moveCmd])

    def moveBy(self, move, pos):
        return tuple(np.add(pos, move))

    def moveByMultiple(self, pos, moves):
        newPositions = []
        for move in moves:
            newPositions.append(self.moveBy(move, pos))
        return newPositions


    # get moves based on a 3x3 array. legal moves are indicated by ones, center is current position
    def getMoves(self):
        indices = np.where(self.allowed == 1)
        indexTuples = list(zip(indices[0], indices[1]))
        # transform from x,y indices to all possible moves
        moves = np.array([[(el - 1) for el in nestedList] for nestedList in indexTuples])
        return moves   


    def getPerpendicularMoves(self, move):
        p1 = np.array([-move[1], move[0]], dtype=np.int32)
        p2 = np.array([move[1], -move[0]], dtype=np.int32)
        return p1, p2


    # set allowed moves for how a map can be walked. For example:
    # (default) left/right/up/down | diagonally/l/r/u/d: | diagonally only:
    # [[0, 1, 0],                  |  [[1, 1, 1],        |  [[1, 0, 1], 
    #  [1, 0, 1],                  |   [1, 0, 1],        |   [0, 0, 0],
    #  [0, 1, 0]]                  |   [1, 1, 1]]        |   [1, 0, 1]]
    def setMoves(self, allowed):
        self.allowed = np.array(allowed, dtype=np.int32)
        self.moves = self.getMoves()
        # filter only relevant directions
        mask = self.allowed == 1
        self.directions = self.allPossibleDirections[mask]
        # zip directions with moves into a dictionary of (move command : move) 
        self.moveCommands.update(zip(self.directions, self.moves))


    # supports multiples of 90 degree turns: 90, 180, 270, 360
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


    def getMovesUpTo(self, maxMoves):
        moves = set()
        for y in range(0, maxMoves + 1):
            for x in range(0, maxMoves - y + 1):
                # if both x and y are not zero
                if y != 0 or x != 0:
                    moves.add((y,x))
                    moves.add((y, -x))
                    moves.add((-y, x))
                    moves.add((-y, -x))
        return [item for item in moves]
    

    
    def getMovesOf(self, maxMoves):
        movesP = combinations_with_replacement(self.moves, maxMoves)
        print(movesP)
        movesPSet = set()
        for mv in movesP:
            movesPSet.add(tuple(np.sum(np.array(mv), axis=0)))
        return movesPSet