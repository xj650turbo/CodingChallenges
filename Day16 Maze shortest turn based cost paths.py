import time
from collections import deque
import os

# imports from my own zutils
from zutils.BaseMap import BaseMap
from zutils.Moves import Moves
from zutils.ColorConsole import ColorCodes, colorString
from zutils.Graph import Graph

class Maze(BaseMap):
    __raindeer = '@'
    __wall = '#'
    __start = 'S'
    __end = 'E'
    __empty = '.'

    def __init__(self, file):
        super().__init__()              # call BaseMap.__init__()
        self.defaultColor = ColorCodes.White
        self.setColorMap({
            self.__wall: ColorCodes.Grey,
            self.__empty: ColorCodes.Grey,
            self.__start: ColorCodes.Green,
            self.__end: ColorCodes.Magenta,
            '<': ColorCodes.Red,
            '>': ColorCodes.Red,
            'v': ColorCodes.Red,
            '^': ColorCodes.Red,
            self.__raindeer: ColorCodes.Red
        })

        self.ignoreCharMap = { '.': ' '}
        self.createFromFile(file)
        self.currPos = self.getIndicesOf(self.__start)[0]
        self.currPosIndicator = '>'
        self.moves = Moves()    # needed by the graph


    def pathCostTurns(self, path):
        prevDir = ''
        cost = 0
        for dir, pos in path:
            if prevDir != '':
                if dir != prevDir:
                    cost += 1000
                cost += 1
            prevDir = dir
        return cost


    def pathCostLength(self, path):
        return len(path)

    
    # run a least cost first (a modified BFS) on the maze to find the first shortest path
    def findEndBFS(self, dir, pos):
        exploredPositions = set()
        dirPos = (dir, tuple(pos))
        queue = deque([(dirPos, [dirPos])])

        self.colorMap['x'] = ColorCodes.Yellow

        while queue:
            dirPos, path = queue.popleft()
            pos = dirPos[1]
            dir = dirPos[0]
            self.currPos = pos

            if pos not in exploredPositions:
                exploredPositions.add(pos)
                cell = self.board[pos[0], pos[1]]

                match cell:
                    case self.__end:
                        break
                    case  self.__wall:
                        continue
                    case self.__empty:
                        self.board[pos[0], pos[1]] = 'x'

                os.system('cls')
                print(self)
                time.sleep(.05)

                # straight first, then right and left
                moveDirs = [dir, self.moves.turn(dir, 90)[0], self.moves.turn(dir, -90)[0]]
                for moveDir in moveDirs:
                    newPos = tuple(self.moves.move(moveDir, pos))
                    newDirPos = (moveDir, newPos)
                    if dir == moveDir:
                        queue.appendleft((newDirPos, path + [newDirPos]))
                    else:
                        queue.append((newDirPos, path + [newDirPos]))
        return path


    def findNumberOfBestSeats(self, allPaths):
        bestSeats = set()
        for path in allPaths:
            for node in path:
                pos = node[0]
                bestSeats.add(pos)
        return len(bestSeats)    



#oldMaze = Maze('input/Day16-mini.txt')
#path = oldMaze.findEndBFS(oldMaze.currPosIndicator, oldMaze.currPos)
#print(oldMaze.pathCostTurns(path))
#time.sleep(3)

fileName = 'input/2024/Day16.txt'
maze = Maze(fileName)

graph = Graph()
graph.buildDirGraphFromMap(maze, maze.moves, 'S', 'E', ['#'])
print(graph.startNode)
print(graph.endNode)

os.system('cls')

shortestPathLength = graph.shortestPathLength()
print("Part 1: shortest path length {0}".format(shortestPathLength))

# in this case allShortestPaths() will not return cycles because there are none in this graph 
# allShortestPaths() is faster than onlyShortestSimplePaths()
shortestPaths = list(graph.allShortestPaths())
combinedPaths = []
for path in shortestPaths:
    combinedPaths.extend(path)
pathDict = {item[0]: (item[2] if item[1] == '.' else item[1]) for item in combinedPaths}
print(maze.overlayPath(pathDict))

bestSeatCount = maze.findNumberOfBestSeats(shortestPaths)
print("Part 2: best seat count {0}".format(bestSeatCount))

if fileName != 'input/2024/Day16.txt':
    graph.plotGraph()
