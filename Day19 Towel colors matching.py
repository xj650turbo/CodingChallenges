# Finds at most one match
# returns 1 if it finds a match at the top level
# item: a string item to search over
# tokens: all possible tokens to search for
# foundTokens: a list of found tokens in the order found
# fromIndex: needed for recursion, 0 when starting, increments by length of token for every recursive call
def tokanizeOne(item, tokens, foundTokens, fromIndex = 0):
    for token in tokens:
        toBeforeIndex = fromIndex + len(token)

        if item[fromIndex:toBeforeIndex] == token:
            if toBeforeIndex >= len(item):
                # we're at the top of the call stack, add the first token as the last one in the list
                foundTokens.append(token)
                return 1    # found 1
            
            numFoundNextLevel = tokanizeOne(item, tokens, foundTokens, toBeforeIndex)
            if numFoundNextLevel > 0:
                # here calls are coming off the stack so add at the beginning of the list to preserve order
                foundTokens.insert(0, token)
                return 1     # found found one, get down the stack returning 1
    return 0    # didn't find any match at this level


# Finds all matching patterns. Uses a shared cache of found counts from top of the stack throughout the recursive call chain  
# item: a string item to search over
# tokens: all possible tokens to search for
# cache: a shared cache of {partial/full towel: numDesigns) 
# fromIndex: needed for recursion, 0 when starting, increments by length of token for every recursive call
def tokanizeAll(item, tokens, cache = {}, fromIndex = 0):
    numFound = 0

    if fromIndex >= len(item):
        return 0
    
    # we've been there before... return the cached item
    if item[fromIndex:] in cache:
        return cache[item[fromIndex:]]
    
    # minor optimization to weed out unecessary looping up the stack
    newTokens = []
    for token in tokens:
        if token in item[fromIndex:]:
            newTokens.append(token)

    for token in newTokens:
        toBeforeIndex = fromIndex + len(token)
        if item[fromIndex:toBeforeIndex] == token:
            if toBeforeIndex == len(item):
                numFound += 1   # we're at the top of the call stack; add 1 to found
            else:
                numFoundRecursively = tokanizeAll(item, newTokens, cache, toBeforeIndex)
                # we're coming down the stack; add number of found in the completed recursive calls chain
                numFound += numFoundRecursively

    cache[item[fromIndex:]] = numFound  # add number of designs for this partial (or full) towel
    return numFound


# read in the file into towels and tokens
tokens = []
towels = []
with open('input/Day19.txt', 'r') as file:
    line = file.readline()
    tokens = line.strip().replace('\n', '').split(', ')
    line = file.readline()
    for line in file:
        towels.append(line.strip().replace('\n', ''))


counts = [0, 0] # will hold part 1 and part 2 answers 
cache = {}      # create a cache of {towel(partial/full): numDesigns), reuse it across all towels
for towel in towels:
    foundTokens = []
    counts[0] += tokanizeOne(towel, tokens, foundTokens)
    counts[1] += tokanizeAll(towel, tokens, cache)
    print("Towel {0}, found tokens {1}".format(towel, foundTokens))

print("Part1: possible designs: {0}".format(counts[0]))
print("Part2: all possible towel designs: {0}".format(counts[1]))