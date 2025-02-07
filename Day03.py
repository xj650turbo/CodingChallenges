import re

#test arrays
code = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
code = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"


with open('input/Day03.txt', 'r') as file:
    code = file.read()

pattern = "mul\(\d+,\d+\)|do\(\)|don\'t\(\)"
instructions = re.findall(pattern, code)

#print(instructions)

sumOfOperations = 0
multiplicationEnabled = True
for instruction in instructions:
    leftParenIdx = instruction.index('(')
    operation = instruction[0:leftParenIdx]
    
    #print(operation)
    match operation:
        case "do":
            multiplicationEnabled = True
        case "don't":
            multiplicationEnabled = False
        case "mul":
            if multiplicationEnabled:
                commaIdx = instruction.index(',')
                op1 = int(instruction[leftParenIdx + 1 : commaIdx])
                op2 = int(instruction[commaIdx + 1 : -1])
                sumOfOperations += op1 * op2

print(sumOfOperations)
