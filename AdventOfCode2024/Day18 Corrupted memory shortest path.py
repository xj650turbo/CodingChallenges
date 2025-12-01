import time
import numpy as np
from collections import deque
import os

# imports from my own zutils
from zutils.BaseMap import BaseMap
from zutils.Moves import Moves
from zutils.ColorConsole import ColorCodes, colorString, clearOutput
from zutils.Graph import Graph


class MemoryGrid(BaseMap):
    __me = '@'
    __wall = '#'
    __start = 'S'
    __end = 'E'
    __empty = '.'

    def __init__(self, fileName, width, height):
        super().__init__()              # call BaseMap.__init__()
        self.defaultColor = ColorCodes.White
        self.setColorMap({
            self.__wall: ColorCodes.Grey,
            self.__empty: ColorCodes.Grey,
            self.__start: ColorCodes.Green,
            self.__end: ColorCodes.Magenta,
            self.__me: ColorCodes.Red,
            '*': ColorCodes.Red
        })
        self.setBoard(np.full((width, height), '.'))
        self.board[0][0] = self.__start
        self.board[width-1, height-1] = self.__end
        self.currPosIndicator = self.__me
        self.currPos = self.getIndicesOf(self.__start)[0]
        self.locationsToCorrupt = []
        self.nextToCorrupt = 0
        self.readCorruptedLocations(fileName)
        self.moves = Moves()    # needed by the graph
        self.graph = None


    # corrupted locations are (X, Y), i.e. horizontal then vertical
    # this is opposite to the array indexing, so switching yo (Y, X)
    def readCorruptedLocations(self, fileName):
        with open(fileName, 'r') as file:
            for line in file:
                line = line.split(',')
                self.locationsToCorrupt.append([int(line[1]), int(line[0])])

    # corrupt N location and remove them from the list of corrupted locations
    # returns last location that was corrupted
    def corruptNLocations(self, num):
        for idx in range(self.nextToCorrupt, self.nextToCorrupt + num):
            if idx < len(self.locationsToCorrupt):
                node = (tuple(self.locationsToCorrupt[idx]), self.board[self.locationsToCorrupt[idx][0], self.locationsToCorrupt[idx][1]])
                if self.graph is not None and node in self.graph.graph.nodes:
                    self.graph.graph.remove_node(node)
                self.board[self.locationsToCorrupt[idx][0], self.locationsToCorrupt[idx][1]] = self.__wall
                # pop the first location from the list, we already coruppted it
                self.nextToCorrupt += 1
            else:
                return None
        # build a graph after the first call
        if self.graph is None:
            self.graph = Graph()
            self.graph.buildGraphFromMap(self, self.moves, 'S', 'E', ['#'])
        return self.locationsToCorrupt[self.nextToCorrupt -1]



memoryGrid = MemoryGrid('input/Day18-mini.txt', 7, 7)
memoryGrid.corruptNLocations(12)
#memoryGrid = MemoryGrid('input/Day18.txt', 71, 71)
#memoryGrid.corruptNLocations(1024)

#memoryGrid.graph.plotGraph()

minimumStepsP1 = memoryGrid.graph.shortestPathLength()

while(1):
    lastCorrupt = memoryGrid.corruptNLocations(1)
    if lastCorrupt is None:
        break

    if memoryGrid.graph.hasPath():
        clearOutput(wait=True)
        paths = memoryGrid.graph.allShortestPaths()
        path = next(paths)
        pathDict = {item[0]: '*' for item in path}
        #print(memoryGrid.overlayPath(pathDict))
        minimumSteps = memoryGrid.graph.shortestPathLength()
        print("Path length after adding a corrupted location {0}".format(minimumSteps))
        #time.sleep(.03)
    else:
        print(memoryGrid)
        # (Y,X) needs to be reversed back to (X,Y) for providing answer to Part 2
        print("Part 2: no path after adding {0},{1}".format(lastCorrupt[1], lastCorrupt[0]))
        break

print("Part 1: minimum steps {0}".format(minimumStepsP1))

