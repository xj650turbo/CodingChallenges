def splitStone(stone):
    if stone == '0':
        return ['1']
    
    digitLen = len(stone)
    if digitLen % 2 == 0:
        return [str(int(stone[0:digitLen//2])), str(int(stone[digitLen//2:digitLen]))]
    else:
        return [str(int(stone)*2024)]


def blink(numTimes, stones):
    inStones = stones
    outStones = stones
    while numTimes > 0:
        outStones = []
        for stone in inStones:
            outStones += splitStone(stone)
        inStones = outStones
        numTimes -= 1
    return outStones


def addToCache(key, value, cache):
    if key not in cache:
        cache[key] = value

#########################################
# cacheStoneSplit: stone --> split stones list. This cache avoids repeated splits
# cacheSplitStonesCountAtLevel: (stone, levelsFromMax) -> count at max level. This cache avoids descending levelsFromMax levels if the count at the max level is already known
#########################################
def blinkForEachNewFirst(numBlinks, stones, currBlink, cacheStoneSplit, cacheSplitStonesCountAtLevel):
    numStonesAtCurrBlink = 0
    levelsFromMax = numBlinks - currBlink
    for stone in stones:
        stoneAtBlink = (stone, levelsFromMax)
        if stoneAtBlink in cacheSplitStonesCountAtLevel:
            numStonesAtCurrBlink += cacheSplitStonesCountAtLevel[stoneAtBlink]
            continue

        if stone in cacheStoneSplit:
            outStones = cacheStoneSplit[stone]
        else:
            outStones = splitStone(stone)
            cacheStoneSplit[stone] = outStones
        
        numStonesAtNextBlink = 0
        if currBlink >= numBlinks - 1:
            numStonesAtNextBlink = len(outStones)
        else:
            numStonesAtNextBlink = blinkForEachNewFirst(numBlinks, outStones, currBlink+1, cacheStoneSplit, cacheSplitStonesCountAtLevel)
        
        numStonesAtCurrBlink += numStonesAtNextBlink
        addToCache(stoneAtBlink, numStonesAtNextBlink, cacheSplitStonesCountAtLevel)
    return numStonesAtCurrBlink



stoneCount = [0, 0]   

with open('input/2024/Day11.txt', 'r') as file:
    line = file.readline()
    line = line.replace('\n', '')

stones = [x for x in line.split()] 

# Part 1
outStones = blink(25, stones)
stoneCount[0] = len(outStones)

# Part 2
cacheStoneSplit = {}                # cacheStoneSplit: stone --> split stones list. This cache avoids repeated splits
cacheSplitStonesCountAtLevel = {}   # cacheSplitStonesCountAtLevel: (stone, levelsFromMax) -> count at max level. This cache avoids descending levelsFromMax levels if the count at the max level is already known
stoneCount[1] = blinkForEachNewFirst(75, stones, 0, cacheStoneSplit, cacheSplitStonesCountAtLevel)

print("\nPart 1 score: {}".format(stoneCount[0]))
print("Part 2 score: {}".format(stoneCount[1]))