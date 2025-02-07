import os
import time
from enum import Enum
import numpy as np
import copy

from zutils.ColorConsole import ColorCodes, colorString 
from zutils.BaseMap import BaseMap
from zutils.Moves import Moves

class Board(BaseMap):
    class MoveStatus(Enum):
        OK = 1
        END = 2
        LOOP = 3
        SPIN = 4

    # "private" members
    __obstacleChar = '#'
    __loopingObstacleChar = 'x'
    __initialDir = '^'

    def __init__(self, fileName, searchForLoopingObstacles):
        super().__init__()  # call BaseMap.__init__()
        self.createCharBoardFromFile(fileName)
        self.setModeForFindingLoopingObstacles(searchForLoopingObstacles)
        self.currPosIndicator = Board.__initialDir
        self.startingPos = self.getIndicesOf(Board.__initialDir)[0]  
        self.currPos = self.startingPos
        self.exitPosition = None
        self.visited = np.zeros(self.board.shape)
        self.path = []                                      #all path turn points with direction of the adjacent obstacle, 
        self.loopingObstacles = set()
        self.countForTurn = {}
        self.loopDetected = False
        self.numTurnsInRow = 0

        self.moves = Moves()
        self.visited[self.currPos[0], self.currPos[1]] = 1
        self.updatePath(self.currPos, None)  #starting point and end point have no obstacle direction


    def __str__(self):
        return self.zoomedLayout()


    def resetCurrentPos(self):
        self.currPos = self.startingPos
        self.currPosIndicator = Board.__initialDir
        self.exitPosition = None


    # in the looping obstacle search mode we want to verify whether a new obstacle causes a loop
    # we also want to display the search using different colors  
    def setModeForFindingLoopingObstacles(self, searchForLoopingObstacles):
        self.searchForLoopingObstacles = searchForLoopingObstacles
        if self.searchForLoopingObstacles:
            # for normal mode 
            charColorMap = {
                '.': ColorCodes.White,
                '^': ColorCodes.White,
                '#': ColorCodes.Red,
                'x': ColorCodes.Green}
        else:
            # for when the board is in the simulation mode 
            charColorMap = {
                '.': ColorCodes.Grey,
                '^': ColorCodes.Grey,
                '#': ColorCodes.Cyan,
                'x': ColorCodes.Magenta}
        self.colorMap = charColorMap


    # can only turn right, i.e. by 90 degrees every turn. return value[0] is the new direction
    def turn(self):
        self.currPosIndicator = self.moves.turn(self.currPosIndicator, 90)[0]


    # move unless out of bounds or loop is detected
    def move(self):
        if self.loopDetected:
            return Board.MoveStatus.LOOP
        
        if self.exitPosition is not None:
            return Board.MoveStatus.END
        
        newPosition = self.moves.move(self.currPosIndicator, self.currPos)
        if self.inBounds(newPosition) == False:
            self.exitPosition = self.currPos
            self.updatePath(self.currPos, None)
            return Board.MoveStatus.END    #if out of bounds 

        if self.board[newPosition[0], newPosition[1]] != self.__obstacleChar:
            # add a check for a looping obstacle if in the obstacle search mode
            if self.searchForLoopingObstacles == True:         
                self.addLoopingObstacle()
            self.numTurnsInRow = 0
            self.currPos = newPosition
            self.visited[self.currPos[0], self.currPos[1]] += 1
            #moved to a new position
            return Board.MoveStatus.OK 
        else:
            # turn right if it's an obstacle
            self.updatePath(self.currPos, self.currPosIndicator)
            self.turn()
            self.numTurnsInRow += 1
            return Board.MoveStatus.OK


    def updatePath(self, pos, dir):
        posDirTuple = (tuple(pos), dir)
        if posDirTuple not in self.countForTurn:
            self.path += [posDirTuple]
            self.countForTurn[posDirTuple] = 1
        else:
            self.countForTurn[posDirTuple] += 1
            if self.countForTurn[posDirTuple] > 2:
                self.loopDetected = True


    def addLoopingObstacle(self):
        if self.searchForLoopingObstacles == False:   
            return False
        
        newObst = self.moves.move(self.currPosIndicator, self.currPos)
        # check if there's already an obstacle in front
        if self.inBounds(newObst) == False or self.board[newObst[0]][newObst[1]] == self.__obstacleChar:
            return False

        # Create a deep copy of the board with new obstacle added and explore the new path to see if it loops
        testBoard = copy.deepcopy(self)
        testBoard.board[newObst[0]][newObst[1]] = self.__obstacleChar
        #the board copy should just explore the new path. It should NOT further check for additional looping obstacles
        testBoard.setModeForFindingLoopingObstacles(False)

        loop = Board.MoveStatus.OK
        while loop == Board.MoveStatus.OK:
            os.system('cls')
            print(testBoard.zoomedLayout(25, 25))
            loop = testBoard.move()
            time.sleep(.05)
        testBoard = None

        # return the new obstacle if loop detected
        if loop == Board.MoveStatus.LOOP:
                if self.visited[newObst[0]][newObst[1]] == 0:
                    newObst = tuple(newObst)
                    self.loopingObstacles.add(newObst)
                    #CHANGE THIS TO SEE OBSTACLES
                    self.board[newObst[0]][newObst[1]] = Board.__loopingObstacleChar
                    return True

        return False


fileName = 'input/Day06-mini3.txt'
board = Board(fileName, searchForLoopingObstacles=True)

loop = Board.MoveStatus.OK
while loop == Board.MoveStatus.OK:
    os.system('cls')
    print(board.zoomedLayout(25, 25))
    loop = board.move()
    time.sleep(.1)

os.system('cls')
print(board)

count = np.count_nonzero(board.visited > 0)
print("Part 1 - visited cells: {0}".format(count))
print("Part 2 - looping obstacles: {0}".format(len(board.loopingObstacles)))
