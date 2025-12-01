import numpy as np

secretNumbers = []

with open('input/2024/Day22.txt', 'r') as file:
    for line in file:
        secretNumbers.append(int(line))

print(secretNumbers)


mix = np.vectorize(lambda sn, v: sn ^ v)
prune = np.vectorize(lambda sn: (sn % 16777216))


s1 = np.vectorize(lambda sn: prune(mix(sn, sn*64)))
s2 = np.vectorize(lambda sn: prune(mix(sn, np.floor(sn/32).astype(int))))
s3 = np.vectorize(lambda sn: prune(mix(sn, sn * 2048)))

evolve = np.vectorize(lambda sn: s3(s2(s1(sn))))

def evolveNth(sn, n):
    while n > 0:
        sn = evolve(sn)
        #print(sn)
        n -= 1
    return sn

evolved2000 = evolveNth(secretNumbers, 2000)
print(evolved2000)

sum2000 = sum(evolved2000)
print(sum2000)