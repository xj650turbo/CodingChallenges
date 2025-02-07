##############################################################################################################
# BaseMap is used for problems requiring a map. It provides default utilities for 
# - creating and Int-based or char-based Map board itself
#   - directly from a file
#   - from a passed in list
#   - from a passed in string
# - readining in a map file
# - printing the board with predefined colors via overloaded BaseMap::__str__()
#   - setColorMap() for defining a color map for printing board characters/digits
#   - setSetIgnoreChars() for ignoring selected characters for the purpose of printing
#   - overlayPath() for overlaying a path dictionary (pos: char/int)
#   - zoomedLayout() for printing at full scale or zommed in to the current position
# - inBound() test for whether a position is in bounds
# - 
##############################################################################################################

import numpy as np

# from my zutils
from zutils.ColorConsole import ColorCodes, colorString

class BaseMap:
    def __init__(self):
        self.ignoreCharMap = {}     # use a map of (ignore_when_val : value_when_ignored). For example: self.ignoreCharMap = {'.': None}
        self.board = None
        self.colorMap = {None: ColorCodes.Red}
        self.defaultColor = ColorCodes.White
        self.currPos = None          # current position
        self.currPosIndicator = None # set to a character or int indicating current position
        self.showMapCoordinates = True


    def __str__(self):
        return self.overlayPath(None)


    def overlayPath(self, pathDict, rangeVert = None, rangeHorz = None):
        ret = ""
        char = ""
        #ret += "0 1 2 3 4 5 6 7 8 9\n"

        rangeVert = range(self.board.shape[0]) if rangeVert is None else rangeVert
        rangeHorz = range(self.board.shape[1]) if rangeHorz is None else rangeHorz

        # Show horizontal and vertical coordinates for convenience. 
        # This can be turned off via showCoordinates() 
        if self.showMapCoordinates:
            if rangeHorz.stop > 100:
                gen100s = (str(int(s/100) % 10) if s > 99 else ' ' for s in rangeHorz)
                ret += " ".join(gen100s) + '\n'
            if rangeHorz.stop > 10:
                gen10s = (str(int(s/10) % 10) if s > 9 else ' ' for s in rangeHorz)
                ret += " ".join(gen10s) + '\n'
            unitsGen = (str(s % 10) for s in rangeHorz)
            ret += " ".join(unitsGen) + '\n'
            ret += "_" * (rangeHorz.stop - rangeHorz.start)*2 + '\n'
                          
        for y in rangeVert:
            for x in rangeHorz:
                if (pathDict is not None) and ((y, x) in pathDict):
                    char = pathDict[(y, x)]
                else:
                    char = self.board[y][x] if self.board[y][x] not in self.ignoreCharMap else self.ignoreCharMap[self.board[y][x]]
                if self.currPos is not None and self.currPosIndicator is not None and np.all(np.array(self.currPos) == [y,x]):
                    char = self.currPosIndicator
                ret += colorString("{0} ".format(char), self.colorMap[char] if char in self.colorMap else self.defaultColor)
            ret += "{0}\n".format("|" + str(y) if self.showMapCoordinates else '')
        return ret
    


    def getZoomRange(self, axis, zoom):
        startend = range(0,0)
        axisDimension = self.board.shape[axis]

        if zoom >= axisDimension:
            startend = range(0, axisDimension)
        elif (self.currPos[axis] - zoom // 2) <= 0:
            startend = range(0, zoom)
        elif (self.currPos[axis] + zoom // 2) >= axisDimension:
            startend = range(axisDimension - zoom, axisDimension)
        else:
            startend = range(self.currPos[axis] - zoom // 2, self.currPos[axis] + zoom // 2)
        return startend

    def zoomedLayout(self, zoomY = None, zoomX = None, displayPathDict = None):
        zoomY = zoomY if zoomY is not None else self.board.shape[0]
        zoomX = zoomX if zoomX is not None else self.board.shape[1]
        topBottom = self.getZoomRange(0, zoomY) # top to bottom zoom window 
        leftRight = self.getZoomRange(1, zoomX) # left to right zoom
        
        return self.overlayPath(displayPathDict, topBottom, leftRight)


    def showCoordinates(self, show):
        self.showMapCoordinates = show


    # creates a base character map
    def read(self, file):
        lol = []
        with open(file, 'r') as file:
            for line in file:
                lol.append([char for char in line.replace('\n', '')])
        return lol


    # creates a Numpy array of characters 
    def createCharBoardFromList(self, list):
        self.board = np.array(list)

    def createIntBoardFromList(self, list):
        self.board = np.array(list, dtype=np.int32)


    # reads the board as a Numpy array of characters, from newline delimited string
    def createCharBoardFromString(self, str):
        lol = []
        splitStr = str.split("\n")
        for line in splitStr:
            if len(line) > 0:
                lol.append([char for char in line])
        self.board = np.array(lol)


    # reads the board as a Numpy array of characters 
    def createCharBoardFromFile(self, file):
        lol = []
        with open(file, 'r') as file:
            for line in file:
                lol.append([char for char in line.replace('\n', '')])
        self.board = np.array(lol)


    # reads the board as a Numpy array of integers 
    def createIntBoardFromFile(self, file):
        lol = []
        with open(file, 'r') as file:
            for line in file:
                lol.append([int(char) for char in line.replace('\n', '')])
        self.board = np.array(lol, dtype=np.int32)


    def setBoard(self, numpyBoard):
        self.board = numpyBoard


    def Board(self):
        return self.board


    def inBounds(self, pos):
        return (pos[0] >= 0 and pos[0] < self.board.shape[0] and pos[1] >= 0 and pos[1] < self.board.shape[1])


    def getIndicesOf(self, searchCellValue):
        indices = np.where(self.board == searchCellValue)
        indexTuples = list(zip(indices[0], indices[1]))
        # transform from x,y tuples to numpy array
        indexArray = np.array([[(el) for el in nestedList] for nestedList in indexTuples])
        return indexArray   


    def setColorMap(self, colorMap): 
        self.colorMap = colorMap


    def setSetIgnoreChars(self, ignoreCharMap): 
        self.ignoreCharMap = ignoreCharMap
