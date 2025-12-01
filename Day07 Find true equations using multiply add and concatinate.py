import operator
from itertools import product

def iterateOperatorsOverOperands(operators, operandCount):
    selfCartesianProduct =  product(operators, repeat=(operandCount-1))
    return selfCartesianProduct

def countValidOperands(result, operands, possibleOperators, outOperators):
    numValidInProduct = 0
    if len(operands) == 0:
        return 0
    if len(operands) == 1:
        return 0
    
    for opList in iterateOperatorsOverOperands(possibleOperators, len(operands)):
        currentResult = operands[0]
        for idx, op in enumerate(opList):
            if op == operator.concat:
                currentResult = (int(operator.concat(str(currentResult), str(operands[idx+1]))))
            else:
                currentResult = op(currentResult, operands[idx+1])
        if result == currentResult:
            numValidInProduct += 1
            outOperators.append(opList)
    return numValidInProduct


equations = []
operators_p1 = [operator.mul, operator.add]                     #for part 1
operators_p2 = [operator.mul, operator.add, operator.concat]    #for part 2

with open('input/2024/Day07.txt', 'r') as file:
    for line in file:
        #line = line.replace('\n', '')
        equation = line.split(": ")
        operands = equation[1].split(' ')
        equations.append((int(equation[0]), list(int(s) for s in operands)))

calibrationResults = [0, 0]
for idx, operators in enumerate([operators_p1, operators_p2]):
    for result, operands in equations:
        validOperators = []
        validEquations = []
        numValid = countValidOperands(result, operands, operators, validOperators)
        if numValid > 0:
            calibrationResults[idx] += result
            validEquations.append((numValid, result, operands, validOperators))

print("Part 1 calibration Result: {0}".format(calibrationResults[0]))
print("Part 2 calibration Result: {0}".format(calibrationResults[1]))
