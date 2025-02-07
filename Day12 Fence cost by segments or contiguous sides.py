import numpy as np

from zutils.ColorConsole import ColorCodes
from zutils.BaseMap import BaseMap
from zutils.Moves import Moves


class Garden(BaseMap):   
    def __init__(self, fileName):
        super().__init__()
        self.createCharBoardFromFile(fileName)
        self.setSetIgnoreChars({
            '.': None
        })
        self.setColorMap({
            0: ColorCodes.Green,
            9: ColorCodes.Red
        })
        self.moves = Moves()        

        #number of occurances of the key, number of fence sections
        self.allVegetablesPlotsAndFenceCells = {}
        self.processedCells = np.array(np.zeros(self.board.shape)) 


    def buildFenceCells(self):
        for y in range(self.board.shape[0]):
            for x in range(self.board.shape[1]):
                self.updateIfNewRegion(y, x)


    def updateIfNewRegion(self, y, x, region=None):
        #if cell hasn't already been processed
        if self.processedCells[y, x] == 0:
            newRegion = region
            cellIdx = np.array([y, x])
            cellVal = self.board[y, x]
            self.processedCells[y, x] = 1
            if newRegion is None:
                if cellVal in self.allVegetablesPlotsAndFenceCells:
                    newRegion = [len(self.allVegetablesPlotsAndFenceCells[cellVal]), [1,0], []]
                    self.allVegetablesPlotsAndFenceCells[cellVal] += [newRegion]
                else:
                    newRegion = [0, [1,0], []]
                    self.allVegetablesPlotsAndFenceCells[cellVal] = [newRegion]
            else:
                newRegion[1][0] += 1
            for moveToNeighbour in self.moves.moves:
                neighbourIdx = cellIdx + moveToNeighbour
                if not self.inBounds(neighbourIdx) or cellVal != self.board[neighbourIdx[0], neighbourIdx[1]]:
                    newRegion[1][1] += 1
                    newRegion[2] += [[moveToNeighbour, np.array([y,x])]]

            cellMoves = self.moves.moves + [[0,0]]
            for moveWithinPlot in cellMoves:
                #nextCellIdx = operationOnTwoLists([y, x], moveWithinPlot, operator.add)
                nextCellIdx = cellIdx + moveWithinPlot
                if self.inBounds(nextCellIdx):
                    if cellVal == self.board[nextCellIdx[0], nextCellIdx[1]]:
                        self.updateIfNewRegion(nextCellIdx[0], nextCellIdx[1], newRegion)


    def buildContiguousFenceSides(self, fenceCells):
        # Fence cells in the list are pointing away from the current cell, i.e. vector outside of the cell
        # Any two cells are contiguous if one cell can be reached via 1 or -1 move along a perpendicular direction from the other  
        # Each fence side is [fence direction, from, to]. From < To when (from[0] < to [0] and from[1]==to[1]) or (from[1] < to [1] and from[0]==to[0])
        fenceSides = []
        for fenceCell in fenceCells:
            fenceCellDir = fenceCell[0]
            fenceCellIdx = fenceCell[1]

            if self.getAdjacentOrContainingFenceSideForCell(fenceCell, fenceSides) is None:
                newFenceSide = [fenceCellDir, fenceCellIdx, fenceCellIdx]
                fenceSides += [newFenceSide]

            # build fence side in the direction perpendicular to where the fence is facing 
            for perpMove in self.moves.getPerpendicularMoves(fenceCellDir):
                nextFenceCellIdx = fenceCellIdx + perpMove
                if self.inBounds(nextFenceCellIdx):
                    while self.board[fenceCellIdx[0], fenceCellIdx[1]] == self.board[nextFenceCellIdx[0], nextFenceCellIdx[1]]:
                        nextCell = [fenceCellDir, nextFenceCellIdx]
                        if self.isCellInFenceCells(nextCell, fenceCells):
                            adjacentFenceSide = self.getAdjacentOrContainingFenceSideForCell(nextCell, fenceSides)
                            if adjacentFenceSide is None:
                                adjacentFenceSide = [fenceCellDir, fenceCellIdx, nextFenceCellIdx]
                                fenceSides += [adjacentFenceSide] 
                            else:
                                self.upadateFenceSide(nextCell, adjacentFenceSide)
                        else:
                            break
                        nextFenceCellIdx = nextFenceCellIdx + perpMove
                        if not self.inBounds(nextFenceCellIdx):
                            break
        return fenceSides
                            

    def isCellInFenceCells(self, fenceCell, fenceCells):
        return any(all(fenceCell[0] == v[0]) and all(fenceCell[1] == v[1]) for v in fenceCells)
    

    # returns the fence side that the cell should be in whether the side contains the cell or is adjancent to the cell 
    def getAdjacentOrContainingFenceSideForCell(self, fenceCell, fenceSides):
        fenceCellDir = fenceCell[0]
        for side in fenceSides:
            fenceSideDir = side[0]
            if (np.all(fenceCellDir == fenceSideDir)):
                fromCell = side[1]
                toCell = side[2]
                if (fenceCell[1][1] == toCell[1] and fenceCell[1][0]+1 >= fromCell[0] and fenceCell[1][0]-1 <= toCell[0]) or (fenceCell[1][0] == toCell[0] and fenceCell[1][1]+1 >= fromCell[1] and fenceCell[1][1]-1 <= toCell[1]):
                    return side
        return None


    # update fence side with a new outside cell that belongs to it
    def upadateFenceSide(self, fenceCell, fenceSide):
        fromCell = fenceSide[1]
        toCell = fenceSide[2]
        if np.all(fenceCell[0] == fenceSide[0]):
            if (fenceCell[1][0] < fromCell[0] and fenceCell[1][1] == fromCell[1]) or (fenceCell[1][1] < fromCell[1] and fenceCell[1][0] == fromCell[0]):
                # the new fenceCell is less so update fromCell (fenceSide[1])
                fenceSide[1] = fenceCell[1]
            elif (fenceCell[1][0] > toCell[0] and fenceCell[1][1] == toCell[1]) or (fenceCell[1][1] > toCell[1] and fenceCell[1][0] == toCell[0]):        
                # the new fenceCell is greater so update toCell (fenceSide[2]
                fenceSide[2] = fenceCell[1]


    def getFenceCost(self, contiguous):
        self.allVegetablesPlotsAndFenceCells = {}
        self.processedCells = np.array(np.zeros(self.board.shape)) 
        self.buildFenceCells()
        cost = 0
        for vegetable, vegetablePlotsAndFenceCells in self.allVegetablesPlotsAndFenceCells.items():
            for plotCountsAndFenceCells in vegetablePlotsAndFenceCells:
                if contiguous:
                    fenceSides = self.buildContiguousFenceSides(plotCountsAndFenceCells[2])
                    cost += plotCountsAndFenceCells[1][0] * len(fenceSides)
                else:
                    cost += plotCountsAndFenceCells[1][0] * plotCountsAndFenceCells[1][1]
        return cost


board = Garden('input/Day12.txt')

cost = board.getFenceCost(contiguous=False)
print("Part 1 - fence cost: {0}".format(cost))

cost = board.getFenceCost(contiguous=True)
print("Part 2 - fence cost: {0}".format(cost))
