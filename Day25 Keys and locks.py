import numpy as np

# imports from my own zutils
from zutils.BaseMap import BaseMap
from zutils.ColorConsole import ColorCodes, colorString, clearOutput



class KeyOrLock(BaseMap):
    filled = '#'
    empty = '.'

    def __init__(self):
        super().__init__()              # call BaseMap.__init__()
        self.defaultColor = ColorCodes.White
        self.setColorMap({
            self.filled: ColorCodes.Red,
            self.empty: ColorCodes.Green
        })
        self.key = None

    


def ReadKeysAndLocks(fileName):
    keys = []
    locks = []
    with open(fileName, 'r') as file:
        while(True):
            keyOrLockStr = ""
            lineCnt = 0
            keyOrLock = KeyOrLock()
            for line in file:
                if lineCnt == 0:
                    keyOrLock.key = line.startswith(keyOrLock.empty)
                lineCnt += 1
                keyOrLockStr += line
                if line == '\n':
                    break

            if len(keyOrLockStr) == 0:
                break
            else:
                keyOrLock.createFromString(keyOrLockStr)
                # each key and lock will have 1 for filled space (#)
                keyOrLock.board = keyOrLock.board=='#'

            if keyOrLock.key:
                keys.append(keyOrLock)
            else:
                locks.append(keyOrLock)
    
    return (keys, locks)


keys, locks = ReadKeysAndLocks('input/2024/Day25.txt')

print("Fits:")
fitCount = 0
for lock in locks:
    for key in keys:
        # 1 will remain where two filled spaces collide. Empty spaces are allowed to collide
        overlap = np.logical_and(lock.board, key.board)
        if np.all(overlap == False):
            fitCount += 1


print("Part 1: fit count {0}".format(fitCount))

