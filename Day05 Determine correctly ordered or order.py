def removeValues(removeList, list):
    return [x for x in list if x not in removeList]


def isPageFirst(x, lst, map):
    for item in lst:
        if (item, x) in map:
            return False
    return True


def checkOrderRecurively(x, lst, map):
    if len(lst) == 0:
        return True

    for item in lst:
        if (item, x) in map:
            return False
        
    return checkOrderRecurively(lst[0], lst[1:], map)


ordering = {}
updates = []

with open('input/2024/Day05.txt', 'r') as file:
    for line in file:
        line = line.replace('\n', '')
        if '|' in line:
            pair = line.split('|')
            ordering[(int(pair[0]), int(pair[1]))] = True
        elif ',' in line:
            updates += [list(int(s) for s in line.split(','))]

#print(ordering)
#print(updates)

score = 0
score2 = 0
for update in updates:
    inOrder = checkOrderRecurively(update[0], update[1:], ordering)
    if inOrder:
        middle = update[len(update) // 2]
        score += middle
    else:
        print("unordered: {0}".format(update))            
        orderedList = []
        for currentSlot in range(len(update)):
            for idx in range(len(update)):
                if update[idx] in orderedList:
                    continue
                isFirst = isPageFirst(update[idx], removeValues(orderedList + update[0:idx+1], update), ordering)
                if isFirst == True:
                    orderedList = orderedList + [update[idx]]
                    break
        print("->ordered: {0}".format(orderedList)) 
        middle = orderedList[len(orderedList) // 2]
        score2 += middle           

print("\nPart 1 score: {}".format(score))
print("Part 2 score: {}".format(score2))
