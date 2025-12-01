import numpy as np
import numpy as cp   # change this to cupy to run using cupy


class ClawMachine:
    costAB = cp.array([3, 1])

    def __init__(self, eqA, eqB, prizeXY):
        self.prizeXY = cp.array(prizeXY)
        self.eqA = cp.array(eqA)
        self.eqB = cp.array(eqB)

    def __str__(self):
        return "Prize XY [{0}]. ButtA XY [{1}], ButtB XY [{2}]".format(self.prizeXY, self.eqA, self.eqB)

    def incrementPrizeXY(self, incr):
        self.prizeXY += incr

    def calcCost(self, solution):
        return cp.dot(solution, ClawMachine.costAB)

    def solveLinearEquations(self):
        # create a matrix of equations, needs to be transposed 
        coefficientsMatrix = cp.array([self.eqA, self.eqB]).T
        # solve A[] * X[] = B[] for X[]
        solution = cp.linalg.solve(coefficientsMatrix, self.prizeXY)

        # verify that integer solution is correct
        intSolution = cp.all(cp.dot(coefficientsMatrix, cp.round(solution)) == self.prizeXY)
        return solution if intSolution else cp.array([0,0])


class PrimitiveClawMachine:
    costA = 3
    costB = 1
    cost = np.array([costA, costB])

    def __init__(self, eqA, eqB, prizeXY):
        self.prizeXY = np.array(prizeXY)
        self.eqA = np.array(eqA)
        self.eqB = np.array(eqB)

    def __str__(self):
        return "Prize XY [{0}]. ButtA XY [{1}], ButtB XY [{2}]".format(self.prizeXY, self.eqA, self.eqB)

    def optimalXYPress(self):
        idx = 0
        costAndABpresses = [0, [0, 0]]

        while idx < 100:
            #pretend idx is the number of presses of A. Calculate presses of button B
            buttAstepsInX = idx * self.eqA[0]
            buttAstepsInY = idx * self.eqA[1]
            if buttAstepsInX <= self.prizeXY[0] and buttAstepsInY < self.prizeXY[1] and ((self.prizeXY[0]-buttAstepsInX) % self.eqB[0]) == 0 and ((self.prizeXY[1]-buttAstepsInY) % self.eqB[1]) == 0:
                #multiples of B presses take us to the prize 
                stepsAlongX = (self.prizeXY[0]-buttAstepsInX) // self.eqB[0]
                stepsAlongY = (self.prizeXY[1]-buttAstepsInY) // self.eqB[1]
                if stepsAlongX == stepsAlongY:
                    presses = [idx, stepsAlongY] 
                    costA = presses[0] * PrimitiveClawMachine.costA
                    costB = presses[1] * PrimitiveClawMachine.costB
                    cost = costA + costB
                    if (costA >= 0 and costB >= 0) and (costAndABpresses[0] == 0 or cost < costAndABpresses[0]):
                        costAndABpresses = [cost, presses]

            #now, pretend idx is the number of presses of B. Calculate presses of button A
            buttBstepsInX = idx * self.eqB[0]
            buttBstepsInY = idx * self.eqB[1]
            if buttBstepsInX <= self.prizeXY[0] and buttBstepsInY < self.prizeXY[1] and ((self.prizeXY[0]-buttBstepsInX) % self.eqA[0]) == 0 and ((self.prizeXY[1]-buttBstepsInY) % self.eqA[1]) == 0:
                #multiples of A presses take us to the prize 
                stepsAlongX = (self.prizeXY[0]-buttBstepsInX) // self.eqA[0]
                stepsAlongY = (self.prizeXY[1]-buttBstepsInY) // self.eqA[1]
                if stepsAlongX == stepsAlongY:
                    presses = [stepsAlongY, idx] 
                    costA = presses[0] * PrimitiveClawMachine.costA
                    costB = presses[1] * PrimitiveClawMachine.costB
                    cost = costA + costB
                    if (costA >= 0 and costB >= 0) and (costAndABpresses[0] == 0 or cost < costAndABpresses[0]):
                        costAndABpresses = [cost, presses]
            idx += 1
        return costAndABpresses


import re

primitiveClawMachines = []
clawMachines = []

def getButton(line):
    buttonEq = re.split("[+,]", line)
    return buttonEq

def getPrize(line):
    prizeEq = re.split("[=,]", line)
    return prizeEq


with open('input/Day13.txt', 'r') as file:
    eof = False
    while not eof:
        buttA = getButton(file.readline())
        buttB = getButton(file.readline())
        prize = getPrize(file.readline())
        primitiveClawMachines.append(PrimitiveClawMachine([int(buttA[i]) for i in [1,3]], [int(buttB[i]) for i in [1,3]], [int(prize[i]) for i in [1,3]]))
        clawMachines.append(ClawMachine([int(buttA[i]) for i in [1,3]], [int(buttB[i]) for i in [1,3]], [int(prize[i]) for i in [1,3]]))
        if file.readline() == "":
            eof = True

cost = 0
for clawMachine in primitiveClawMachines:
    # Part 1
    costAndPresses = clawMachine.optimalXYPress()
    cost += costAndPresses[0]
print("Part 1 button press cost: {0}".format(int(cost)))

cost = cp.float64(0)
for clawMachine in clawMachines:
    # part 2
    clawMachine.incrementPrizeXY(10000000000000)

    solution = clawMachine.solveLinearEquations()
    cost += clawMachine.calcCost(solution)
print("Part 2 button press cost: {0}".format(int(cost)))
