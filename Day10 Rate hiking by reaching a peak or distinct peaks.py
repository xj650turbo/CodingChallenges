import numpy as np

from zutils.ColorConsole import ColorCodes
from zutils.BaseMap import BaseMap
from zutils.Moves import Moves


class Map(BaseMap):   
    def __init__(self, file):
        super().__init__()
        self.createIntBoardFromFile(file)

        self.setSetIgnoreChars({
            '.': None
        })

        self.setColorMap({
            0: ColorCodes.Green,
            9: ColorCodes.Red
        })

        self.moves = Moves()        

        trailHeadIndices = np.where(self.board == 0)
        self.trailHeadList = list(zip(*trailHeadIndices))


    def rateTrailhead(self, idx, peaksSoFar, considerDistinctTrails):
        rating = 0
        valueAtIdx = self.Board()[idx]
        if valueAtIdx in self.ignoreCharMap:
            return 0

        if valueAtIdx == 9 and idx not in peaksSoFar:
            if not considerDistinctTrails:
                peaksSoFar += [idx]
            return 1
        
        for move in self.moves.moves:
            nextIdx = tuple(np.add(idx, move))
            if not self.inBounds(nextIdx):
                continue
            valueAtNextIdx = self.board[nextIdx]
            if valueAtNextIdx is not None and valueAtNextIdx - valueAtIdx == 1:        
                #print((idx, move, nextIdx, valueAtIdx, valueAtNextIdx))
                rating += self.rateTrailhead(nextIdx, peaksSoFar, considerDistinctTrails)
            else:
                continue
        return rating
    

    def rateTrailheads(self, considerDistinctTrails):
        overallRating = 0
        for trailHead in self.trailHeadList:
            peaksSoFar = []
            rating = self.rateTrailhead(trailHead, peaksSoFar, considerDistinctTrails)
            overallRating += rating
            #print("Rating {0}".format(rating))
        return overallRating

board = Map('input/Day10.txt')
print(board)

rating = board.rateTrailheads(considerDistinctTrails = False)
print("Part 1 - rating: {0}".format(rating))

rating = board.rateTrailheads(considerDistinctTrails = True)
print("Part 2 - rating: {0}".format(rating))


