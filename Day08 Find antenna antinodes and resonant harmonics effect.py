import numpy as np
from itertools import combinations
from zutils.BaseMap import BaseMap
from zutils.ColorConsole import ColorCodes

class Map(BaseMap):
    __spaceChar = '.'
    
    def __init__(self, fileName):
        super().__init__()  # call BaseMap.__init__()
        self.createCharBoardFromFile(fileName) #np.array(board)
        self.showCoordinates(False)
        self.setColorMap({'.': ColorCodes.Grey})
        self.antennas = {}
        self.antinodes = np.zeros(self.board.shape)
        # find antennas
        for y in range(self.board.shape[0]):
            for x in range(self.board.shape[1]):
                c = str(self.board[y][x]) 
                if c != Map.__spaceChar:
                    if c in self.antennas:
                        self.antennas[c].append((y, x))
                    else:
                        self.antennas[c] = [(y, x)]


    def markAntinodes(self, antennas, resonantHarmonics):
        # Use distance vector to walk in the positive distance direction for the first antenna and in the negative direction for the second one.
        ant1ToAnt2Dist = tuple(np.subtract(antennas[0], antennas[1]))
        for antIdx, posOrNegOffset in enumerate([1, -1]):
            antenna = antennas[antIdx]
            # include antenna location (0) when considering resonant harmonics. 
            # Otherwise disregard it by setting offset to 1 for the first antenna and -1 for the second one
            nextHarmonicOffset = 0 if resonantHarmonics else posOrNegOffset   
            loop = True 
            while(loop):
                node = tuple(np.add(antenna, tuple(np.multiply(ant1ToAnt2Dist, nextHarmonicOffset))))
                nodeInBounds = self.inBounds(node) 
                if nodeInBounds:
                    self.antinodes[node[0], node[1]] = 1
                
                loop = nodeInBounds and resonantHarmonics
                nextHarmonicOffset += posOrNegOffset
        

    def detectAntinodes(self, resonantHarmonics):
        self.antinodes = np.zeros(self.board.shape)
        for key, value in self.antennas.items():
            combs = combinations(value, 2)
            for comb in combs:
                self.markAntinodes(comb, resonantHarmonics)


board = Map('input/Day08.txt')
print(board)

board.detectAntinodes(resonantHarmonics=False)
count = np.count_nonzero(board.antinodes > 0)
print("Part 1 - antinodes: {0}".format(count))


board.detectAntinodes(resonantHarmonics=True)
count = np.count_nonzero(board.antinodes > 0)
print("Part 1 - antinodes: {0}".format(count))