# import from Z Utilities
import zutils.Moves as m

def getElemAtOffset(row, col, arr):
    if row < 0 or col < 0 or row >= len(arr) or col >= len(arr[0]):
        return ''
    else:
        return arr[row][col]


lol = []
with open('input/Day04.txt', 'r') as file:
    for line in file:
        lol.append([char for char in line.replace('\n', '')])

pattern = "XMAS"
searchStarting = 'X'
shape = (len(lol), len(lol[0]))

# legal moves from center are indicated by ones, center is current position
# allows to move only left, right, up, down and diagonally
moveDiagLRDU = m.Moves([ 
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
    ])

count = 0
for row in range(shape[0]): 
    for col in range(shape[1]):
        if lol[row][col] == searchStarting:
            for rowStep, colStep in moveDiagLRDU.moves:
                potentialMatch = "".join(getElemAtOffset(row + rowStep * numSteps, col + colStep * numSteps, lol) for numSteps in range(len(pattern)))
                count += 1 if (potentialMatch == pattern) else 0

print("Count for part #1: {0}".format(count))


# allows to move only left_up and left-down
moveDirectionsFromCenter = m.Moves([ 
    [1, 0, 0],
    [0, 0, 0],
    [1, 0, 0]
    ])

patterns = ["MAS", "SAM"]
searchAround = 'A'

count = 0
for row in range(shape[0]): 
    for col in range(shape[1]):
        if lol[row][col] == searchAround:
            crossMatches = 0
            for rowStep, colStep in moveDirectionsFromCenter.moves:
                potentialMatch = "".join(getElemAtOffset(row + rowStep * numSteps, col + colStep * numSteps, lol) for numSteps in [-1,0,1])
                crossMatches += 1 if (potentialMatch in patterns) else 0
            if crossMatches == 2:
                count += 1


print("Count for part #2: {0}".format(count))


