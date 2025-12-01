import numpy as np

#test arrays
arr1 = np.array([3,4,2,1,3,3])
arr2 = np.array([4,3,5,3,9,3])

list1 = []
list2 = []

with open('input/2024/Day01.txt', 'r') as file:
    for line in file:
        split = line.split("   ")
        list1.append(int(split[0]))
        list2.append(int(split[1]))

arr1 = np.array(list1)
arr2 = np.array(list2)

arr1.sort(kind='mergesort')
arr2.sort(kind='mergesort')
distances = abs(arr1 - arr2)

distance = distances.sum()
print("Distance: " + str(distance))             #part 1 answer: 1889772

cache = {}
idx1 = 0
idx2 = 0
similarity = 0
while idx1 < len(arr1):
    el1 = arr1[idx1]
    idx1 += 1
    if el1 in cache:
        similarity += el1 * cache[el1]
        continue
    
    el1Repeated = 0
    while idx2 < len(arr2) and arr2[idx2] <= el1:
        el2 = arr2[idx2]
        if el1 == el2:
           el1Repeated += 1
        idx2 += 1
    cache[el1] = el1Repeated
    similarity += el1 * el1Repeated

print("Similarity: " + str(similarity))       #part 2 answer: 23228917