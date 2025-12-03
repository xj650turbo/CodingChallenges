import numpy as np

secretNumbers = []

with open('input/2024/Day22.txt', 'r') as file:
    for line in file:
        secretNumbers.append(int(line))

secretNumbers = np.array(secretNumbers)
print(secretNumbers)


mix = lambda sn, v: sn ^ v
prune = lambda sn: (sn % 16777216)

s1 = lambda sn: prune(mix(sn, sn*64))
s2 = lambda sn: prune(mix(sn, np.floor(sn/32).astype(int)))
s3 = lambda sn: prune(mix(sn, sn * 2048))

evolve = np.vectorize(lambda sn: s3(s2(s1(sn))))

totalPriceForSeqOf4 = {}
setBuyerSequence = set()

def evolveNth(sn, nTimes):
    seqOf4 = np.zeros((len(sn), 4)).astype(int)
    prevSnPrice = None
    i = 1
    while i <= nTimes:
        seqOf4 = np.roll(seqOf4, -1, axis=1)
        sn = evolve(sn)
        snPrice = sn % 10
        if prevSnPrice is not None:
            diff = snPrice - prevSnPrice
            # set the last column of the 2d array
            seqOf4[:, -1] = diff

            if i > 4:
                for index, item in enumerate(seqOf4):
                    item = tuple(item.tolist())
                    buyerSequenceTup = (index, item)
                    if buyerSequenceTup not in setBuyerSequence:
                        setBuyerSequence.add(buyerSequenceTup)
                        if item in totalPriceForSeqOf4:
                            totalPriceForSeqOf4[item] += int(snPrice[index])
                        else:
                            totalPriceForSeqOf4[item] = int(snPrice[index])

                highestPrice = max(totalPriceForSeqOf4.values())
                highestPriceSequence = max(totalPriceForSeqOf4, key=totalPriceForSeqOf4.get)
                print(f"{i} Highest total bananas: {highestPrice}, sequence: {highestPriceSequence}")
        prevSnPrice = snPrice
        i += 1
    return sn, totalPriceForSeqOf4

evolved2000, totalPriceForSeqOf4 = evolveNth(secretNumbers, 2000)
print(evolved2000)

print("")
sum2000 = sum(evolved2000)
print(f"Part1: {sum2000}")

highestPrice = max(totalPriceForSeqOf4.values())
highestPriceSequence = max(totalPriceForSeqOf4, key=totalPriceForSeqOf4.get)
print(f"Part2: Highest total bananas: {highestPrice}, sequence: {highestPriceSequence}")