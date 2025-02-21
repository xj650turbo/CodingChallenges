import time
import numpy as np

# imports from my own zutils
from zutils.BaseMap import BaseMap
from zutils.Moves import Moves
from zutils.ColorConsole import ColorCodes, colorString, clearOutput
from zutils.Graph import Graph
import time


class RaceTrack(BaseMap):
    __me = '@'
    __wall = '#'
    __start = 'S'
    __end = 'E'
    __empty = '.'

    def __init__(self, fileName):
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
        self.createFromFile(fileName)
        self.currPosIndicator = self.__me
        self.currPos = self.getIndicesOf(self.__start)[0]
        self.moves = Moves()    # needed by the graph
        self.graph = Graph()


    # Part 1: find cheats that save at least savingAtLeast 
    def findCheatsP1(self, savingAtLeast):
        cheatCounts = {}    # represents how many cheat counts of a specific cost savings there are 
        self.graph.buildGraphFromMap(self, self.moves, 'S', 'E', ['#'])
        costAndShortestPaths = self.graph.dzikstraAllLeastCostPaths(self.graph.startNode, self.graph.endNode)

        endPath = costAndShortestPaths[self.graph.endNode][1][0]   # since there is a single path
        for node in endPath:
            currPos = node[0]
            self.currPos = currPos
            for wallMoveCmd in self.moves.moveCommands:
                wallPos = self.moves.move(wallMoveCmd, currPos)
                if self.inBounds(wallPos) and self.board[wallPos[0], wallPos[1]] == self.__wall:
                    for cheatMoveCmd in self.moves.moveCommands:
                        cheatPos = tuple(int(x) for x in self.moves.move(cheatMoveCmd, wallPos))
                        if self.inBounds(cheatPos):
                            cheatCell = self.board[cheatPos[0], cheatPos[1]]
                            cheatNode = (cheatPos, cheatCell)
                            if cheatNode in costAndShortestPaths:
                                cheatCostSavings = costAndShortestPaths[cheatNode][0] - costAndShortestPaths[node][0] - 2
                                if cheatCostSavings >= savingAtLeast:
                                    if cheatCostSavings not in cheatCounts:
                                        cheatCounts[cheatCostSavings] = 1
                                    else:
                                        cheatCounts[cheatCostSavings] += 1
        return sum(cheatCounts.values())


    # Part 2: find cheats that make at most maxMoves and that save at least savingAtLeast 
    def findCheatsP2(self, maxMoves, savingAtLeast):
        cheats = {}
        self.graph.buildGraphFromMap(self, self.moves, 'S', 'E', ['#'])
        costAndShortestPaths = self.graph.dzikstraAllLeastCostPaths(self.graph.startNode, self.graph.endNode)
        # get all possible moves when moving up to maxMoves times
        shortcutMoves = self.moves.getMovesUpTo(maxMoves)
        shortestPath = costAndShortestPaths[self.graph.endNode][1][0]   # since there is a single path
        for node in shortestPath:
            self.findCheatsInArea(node, shortcutMoves, costAndShortestPaths, savingAtLeast, cheats)    # this is the first move
        return cheats

    # Part 2: helper function finding cheats aroundNode given all shortcutMoves along the shortest path with cost 
    # It updates cheats with the minimum value of saved cost, that is greater than savingAtLeast (any savings less than that are ignored)
    def findCheatsInArea(self, aroundNode, shortcutMoves, costAndShortestPaths, savingAtLeast, cheats):
        clearOutput(wait=True)
        currPos = aroundNode[0]
        currCost = costAndShortestPaths[aroundNode][0]
        self.currPos = currPos
        shortcutPositions = []
        # for every possible shortcut move (represented by the shortcutMoves list)
        for move in shortcutMoves:
            cheatPos = self.moves.moveBy(move, currPos)
            if self.inBounds(cheatPos):
                cheatCell = self.board[cheatPos[0], cheatPos[1]]
                cheatNode = (cheatPos, cheatCell)
                shortcutPositions.append(cheatPos)
                if cheatNode in costAndShortestPaths:
                    cheatKey = (currPos, cheatPos)
                    cheatCost = costAndShortestPaths[cheatNode][0]
                    costSavings = cheatCost - currCost - abs(cheatPos[0] - currPos[0]) - abs(cheatPos[1] - currPos[1])
                    if costSavings >= savingAtLeast:
                        if cheatKey not in cheats:
                            cheats[cheatKey] = costSavings
                        else:
                            if costSavings < cheats[cheatKey]:
                                cheats[cheatKey] = costSavings
        print(self.overlayPath(shortcutPositions))
        time.sleep(.04)



cheatCounts = [0,0]
savingAtLeast = 1
maxMoves = 3

raceTrack = RaceTrack('input/Day20-mini.txt')

#part 1
cheatCounts[0] = raceTrack.findCheatsP1(savingAtLeast)

#part 2
cheats = raceTrack.findCheatsP2(maxMoves, savingAtLeast)
cheatCounts[1] = len(cheats)

print("Part 1: count of cheats that save {1}+ picoseconds with 2 cheats allowed {0}".format(cheatCounts[0], savingAtLeast))
print("Part 2: count of cheats that save {1}+ picoseconds with {2} cheats allowed  {0}".format(cheatCounts[1], savingAtLeast, maxMoves))

