# %%
import math
import numpy as np

#test arrays
lolTest = np.array(
[[7, 6, 4, 2, 1],
 [1, 2, 7, 8, 9],
 [9, 7, 6, 2, 1],
 [1, 3, 2, 4, 5],
 [8, 6, 4, 4, 1],
 [1, 3, 6, 7, 9]]
)

inputListOfLists = []

with open('Day2.txt', 'r') as file:
    for line in file:
        split = line.split(" ")
        rowList = []
        for el in split:
            rowList.append(int(el))
        inputListOfLists.append(rowList)

############################################
# Solve part 1: False, solve part 2: True
############################################
solvePartTwo = True    

safeCount = 0
for list in inputListOfLists:
    arr = np.array(list)
    rowSafe = False

    withoutIdx = arr.size
    while withoutIdx >= 0:
        newArr = arr if withoutIdx >= arr.size else np.delete(arr, withoutIdx)
        #print("Original row: " + str(arr) + ", removed one from row: " + str(newArr))
        withoutIdx -= 1

        differenceAndSign = (newArr[1:] - newArr[:-1]) 
        differentBy1to3 = np.logical_and( np.all(np.greater(abs(differenceAndSign), 0), axis=0), np.all(np.less(abs(differenceAndSign), 4), axis=0))
        allIncrOrDecr = np.logical_or( np.all(np.greater(differenceAndSign, 0), axis=0), np.all(np.less(differenceAndSign, 0), axis=0))

        rowSafe = np.logical_and(differentBy1to3, allIncrOrDecr)
        if rowSafe or not solvePartTwo:
            break

    #print(rowSafe)    
    if rowSafe:
        safeCount += 1
print(safeCount)

# %%



