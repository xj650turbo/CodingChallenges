import os
import re
import copy
import time

# import from Z Utilities
import zutils.ColorConsole as cc


##############################################################################
# Computer class to handle running instructions and reversing registerA values
##############################################################################
class Computer:
    def __init__(self):
        self.registerA = 0
        self.registerB = 0
        self.registerC = 0
        self.program = []
        self.maxProgramPtr = 0
        self.instructionPointer = 0
        self.outputPointer = 0
        self.output = []


    def __str__(self):
        ret = "Register A: {0}\n".format(self.registerA)
        ret += "Register B: {0}\n".format(self.registerB)
        ret += "Register C: {0}\n".format(self.registerC)
        ret += "Output: previous output {1})\n".format(self.outputPointer, self.readPrevOutputValue())
        for idx, output in enumerate(self.output):
            separator = ',' if idx < self.outputPointer else ''
            if idx == self.outputPointer -1:
                ret += "{0}<-{1}".format(cc.colorString(output, cc.ColorCodes.Red), separator)
            else:
                ret += "{0}{1}".format(output, separator)
        opcode, operand, comboOperand = self.nextInstruction()
        ret += "\nProgram nextIstr #{0}, (opcode, operand, comboOp) ({1}, {2}, {3}):\n".format(self.instructionPointer, opcode, operand, comboOperand)
        for idx, op in enumerate(self.program):
            separator = ',' if idx < self.maxProgramPtr else ''
            if idx == self.instructionPointer:
                ret += "->{0}{1}".format(cc.colorString(op, cc.ColorCodes.Green), separator)
            else:
                ret += "{0}{1}".format(op, separator)
        return ret
    

    def __eq__(self, other):
        if not isinstance(other, Computer):
            return False
        return (self.registerA == other.registerA and
            self.registerB == other.registerB and
            self.registerC == other.registerC and
            self.program == other.program and
            self.maxProgramPtr == other.maxProgramPtr and
            self.instructionPointer == other.instructionPointer and
            self.outputPointer == other.outputPointer and 
            self.output == other.output)


    def outputValue(self, value):
        self.output += [value]
        self.outputPointer += 1


    def readPrevOutputValue(self, howFarBack = -1):
        if self.outputPointer + howFarBack < 0:
            return 0
        else:
            return (self.output[self.outputPointer + howFarBack])


    def outputAsStr(self):
        return ",".join(map(str, self.output))


    def readProgram(self, file):
        with open(file, 'r') as file:
            for line in file:
                if line.startswith("Register"):
                    split = re.split('[ :]', line)
                    match split[1]:
                        case 'A':
                            self.registerA = int(split[3])
                        case 'B':
                            self.registerB = int(split[3])
                        case 'C':
                            self.registerC = int(split[3])
                elif line.startswith("Program"):
                    line = line.removeprefix("Program: ")
                    split = re.split('[,]', line)
                    self.program = [int(s) for s in split]
                    self.maxProgramPtr = len(split) -1


    def nextInstruction(self):
        ret = (None, None, None)
        if self.instructionPointer <= self.maxProgramPtr and self.instructionPointer >= 0:
            opcode = self.program[self.instructionPointer]
            if self.instructionPointer + 1 <= self.maxProgramPtr:
                operand = self.program[self.instructionPointer + 1]
                comboOperand = self.getComboOperand(self.program[self.instructionPointer + 1])
                ret = (opcode, operand, comboOperand)           
        return ret
    

    def prevInstruction(self):
        if self.instructionPointer <= 0:
            ret = (None, None, None)
        prevInstrIdx = self.instructionPointer - 2
        opcode = self.program[prevInstrIdx]
        operand = self.program[prevInstrIdx + 1]
        comboOperand = self.getComboOperand(self.program[prevInstrIdx + 1])
        ret = (opcode, operand, comboOperand)           
        return ret


    def getComboOperand(self, operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.registerA
            case 5:
                return self.registerB
            case 6:
                return self.registerC
            case 7:
                return None


    def executeNext(self):
        opcode, operand, comboOperand = self.nextInstruction()
        if opcode is None:
            return False
        incrementPointer = True
        match opcode:
            case 0: # adv: A = (int(A/2^comboOperand)
                self.registerA = int(self.registerA / (2 ** comboOperand))
            case 1: # bxl: B = B XOR operand
                self.registerB = self.registerB ^ operand
            case 2: # bst: B = comboOperand mod 8
                self.registerB = comboOperand % 8
            case 3: # jnz: jump to operand
                if self.registerA != 0:
                    self.instructionPointer = operand
                    incrementPointer = False
            case 4: # bxc: B = B XOR C
                self.registerB = self.registerB ^ self.registerC
            case 5: # out
                val = comboOperand % 8            
                self.outputValue(val)
            case 6: # bdv: B = (int(A/2^comboOperand) 
                self.registerB = int(self.registerA / (2 ** comboOperand))
            case 7: # cdv: C = (int(A/2^comboOperand) 
                self.registerC = int(self.registerA / (2 ** comboOperand))

        if incrementPointer:
            self.instructionPointer += 2
        return True


    def testOneCycleForward(self):
        testComp = copy.deepcopy(self)
        while testComp.instructionPointer != len(testComp.program) - 2:
            testComp.executeNext() 
        return testComp


    def runToTheEnd(self):
        while self.executeNext():
            os.system('cls')
            print(self)
            print("\n")
            time.sleep(.05)       


    def getCompForReversing(self):
        revComp = copy.deepcopy(self)
        revComp.registerA = 0
        revComp.instructionPointer = len(revComp.program)
        revComp.output = revComp.program.copy()
        revComp.outputPointer = len(revComp.output)
        return revComp


    def generatePossibleCompsOneCycleBack(self):
        quotient = self.registerA
        divisor = 2 ** 3
        for remainder in range(divisor):
            prevMe = copy.deepcopy(self)
            if prevMe.outputPointer == 0:
                return 
            del prevMe.output[prevMe.outputPointer-1]
            prevMe.outputPointer -= 1
            prevMe.instructionPointer = 0
   
            dividend = quotient * divisor
            prevMe.registerA = dividend + remainder
            yield prevMe


    def generateAllValidOneCycleBack(self):
        prevCompGenerator = self.generatePossibleCompsOneCycleBack()
        for prevComp in prevCompGenerator:
            testComp = prevComp.testOneCycleForward()
            if self.output == testComp.output:
                yield prevComp



    def searchDepthFirst(self, numLevels, currLevel = 1):
        generatePreviousValid = self.generateAllValidOneCycleBack()
        #print("{0}>".format(currLevel), end='')

        for validPrev in generatePreviousValid:
            if currLevel == numLevels:
                return validPrev
            validPrevPrev = validPrev.searchDepthFirst(numLevels, currLevel + 1)
            if validPrevPrev is not None:
                return validPrevPrev
        return None


########################################################################
# main
########################################################################
computer = Computer()
computer.readProgram('input/Day17.txt')
revComp = computer.getCompForReversing()

computer.runToTheEnd()
print("Part 1 answer ^^^^^ {0}".format(computer.output))

nLevelsBackComp = revComp.searchDepthFirst(16)
print("\nPart 2 answer {0}:\n{1}".format(nLevelsBackComp.registerA, nLevelsBackComp))





