class Fragmentor:
    def __init__(self, diskMap):
        # disk map as string and its indices
        self.diskMap = diskMap
        self.mapLength = len(diskMap)
        self.frontIdx = 0
        self.endIdx = self.mapLength - 1
        #a list of disk blocks with details with its indices
        self.diskBlocks = []                # (fileId, numBlocks, startIdx, endIdx, True)
        self.maxBlockIdx = 0                # used for adding files, the maximum block in diskBlocks                   

        self.currentFreeblocks = 0    
        self.processingFile =  None         # used for moving a file to free space (fileId, remainingBlocks)
        self.filesystemChecksum = 0


    def __str__(self):
        ret = ""
        for seg in self.diskBlocks:
            ret += (str(seg[0]) if seg[0] != -1 else ".") * seg[1]
        return ret
        

    #get from front if filling of following free space is done 
    def nextFromFront(self):
        if (self.frontIdx <= self.endIdx and self.currentFreeblocks == 0):
            file = self.getFromDiskMap(self.frontIdx)
            if file is not None:
                if file[0] >= 0:
                    self.addFile(file)
                else:
                    self.currentFreeblocks = file[1]
                self.frontIdx += 1
                return True
        return False

    
    #get from end if fragmenting of the current file is complete 
    def nextFromEnd(self):
        if (self.frontIdx <= self.endIdx and self.processingFile is None):
            file = self.getFromDiskMap(self.endIdx)
            if file[0] > 0:
                self.processingFile = file
                self.endIdx -= 1
            self.endIdx -= 1
            return True                    
        return False
    
 
    # (id, numBlocks), file ID or -1 for free space
    def getFromDiskMap(self, index):
        if index >= 0 and index < self.mapLength:
            id = index // 2 if index % 2 == 0 else -1
            numBlocks = int(self.diskMap[index])
        return [id, numBlocks]


    # each block has id, start and end index
    def addFile(self, file):
        #don't add a segment with 0 blocks
        if file[1] > 0:
            self.diskBlocks += [file]
            self.maxBlockIdx += file[1]


    def calcChecksum(self):
        self.filesystemChecksum = 0
        segIdx = 0
        for seg in self.diskBlocks:
            if seg[0] >= 0:   # if not free space
                for fileIdx in range(segIdx, segIdx + seg[1]):
                    self.filesystemChecksum += seg[0] * fileIdx
            segIdx += seg[1]
        return self.filesystemChecksum
    

    def fragmentCurrent(self):
        if self.processingFile is not None and (self.currentFreeblocks > 0 or self.endIdx < self.frontIdx):
            if self.processingFile[1] <= self.currentFreeblocks or self.endIdx < self.frontIdx:
                self.addFile(self.processingFile)
                self.currentFreeblocks -= self.processingFile[1]
                self.processingFile = None
            else:
                partialFile = (self.processingFile[0], self.currentFreeblocks)
                self.addFile(partialFile)
                self.processingFile = (self.processingFile[0], self.processingFile[1] - self.currentFreeblocks)
                self.currentFreeblocks = 0
        return True if self.currentFreeblocks == 0 else False


    def done(self):
        return self.endIdx < self.frontIdx and self.processingFile is None
    

    def performFragmentation(self):
        while not self.done():
            while self.nextFromFront():
                pass
            while self.nextFromEnd():
                pass
            self.fragmentCurrent()


class Defragmentor:
    def __init__(self, diskMap):
        # disk map as string and its indices
        self.diskMap = diskMap
        self.mapLength = len(diskMap)
 
        #a list of disk blocks with details with its indices
        self.diskBlocks = []                # (fileId, numBlocks, startIdx, endIdx, True)
        self.maxSegmentIdx = 0                #used for adding files, the maximum block in diskBlocks                   
        self.frontSegmentIdx = 0
        self.endSegmentIdx = 0

        self.filesystemChecksum = 0

    def __str__(self):
        ret = ""
        for seg in self.diskBlocks:
            ret += (str(seg[0]) if seg[0] != -1 else ".") * seg[1]
        return ret

    # (id, numBlocks), file ID or -1 for free space
    def getFromDiskMap(self, index):
        if index >= 0 and index < self.mapLength:
            id = index // 2 if index % 2 == 0 else -1
            numBlocks = int(self.diskMap[index])
        return [id, numBlocks]


    #build a list of all blocks including free space
    def buildAllDiskBlocks(self):
        frontIdx = 0
        endIdx = self.mapLength - 1
        while frontIdx <= endIdx:
            file = self.getFromDiskMap(frontIdx)
            self.addFile(file)
            frontIdx += 1          
        # reset Segment indices
        self.frontSegmentIdx = 0
        self.endSegmentIdx = len(self.diskBlocks) - 1


    # each block has id, start and end index
    def addFile(self, file):
        startIdx = self.maxSegmentIdx
        endIdx = self.maxSegmentIdx + file[1] - 1
        if endIdx >= startIdx:
            self.diskBlocks += [file]
            self.maxSegmentIdx += file[1]

    
    def calcChecksum(self):
        self.filesystemChecksum = 0
        segIdx = 0
        for seg in self.diskBlocks:
            if seg[0] >= 0:   # if not free space
                for fileIdx in range(segIdx, segIdx + seg[1]):
                    self.filesystemChecksum += seg[0] * fileIdx
            segIdx += seg[1]
        return self.filesystemChecksum
 

    def moveNextFileToFirstFreeSpace(self):
        nextSegFromEnd = None
        while nextSegFromEnd is None and self.endSegmentIdx > 0:
            if self.endSegmentIdx > self.frontSegmentIdx: 
                nextSegFromEnd = self.diskBlocks[self.endSegmentIdx]
                if nextSegFromEnd[0] == -1:
                    nextSegFromEnd = None
                else:
                    segBefore = self.diskBlocks[self.endSegmentIdx-1]
                    segAfter = None if self.endSegmentIdx >= len(self.diskBlocks)-2 else self.diskBlocks[self.endSegmentIdx+1]
            self.endSegmentIdx -= 1
        

        if self.endSegmentIdx > self.frontSegmentIdx:
            for segIdx in range(0, self.endSegmentIdx+1):
                freeSegment = self.diskBlocks[segIdx] if self.diskBlocks[segIdx][0] == -1 else None

                if freeSegment is not None:    #it's free space
                    numFileBlocks = nextSegFromEnd[1]
                    numFreeSpaceBlocks = freeSegment[1]    
                    if numFileBlocks <= numFreeSpaceBlocks:
                        freeSpaceRemaining = numFreeSpaceBlocks - numFileBlocks

                        #convert free segment on left to file blocks. Change the To index, the From index doesn't change
                        freeSegment[0] = nextSegFromEnd[0]          
                        freeSegment[1] = nextSegFromEnd[1]    

                        #convert segment to free space, indices remain the same. Merge neighbouring segments
                        convertedSeg = None
                        if segBefore[0] == -1:
                            segBefore[0] = -1
                            segBefore[1] = segBefore[1] + numFileBlocks
                            convertedSeg = segBefore
                            convertedIdx = self.endSegmentIdx
                            self.diskBlocks.pop(self.endSegmentIdx+1)
                        else:
                            nextSegFromEnd[0] = -1
                            nextSegFromEnd[1] = numFileBlocks
                            convertedSeg = nextSegFromEnd
                            convertedIdx = self.endSegmentIdx+1

                        if segAfter is not None and segAfter[0] == -1:
                            convertedSeg[0] = -1
                            convertedSeg[1] = convertedSeg[1] + segAfter[1]
                            self.diskBlocks.pop(convertedIdx+1)

                        # if there was more free space than the moved segment, add a free space segment after the segment at segIdx
                        if freeSpaceRemaining > 0:
                            self.diskBlocks.insert(segIdx+1, [-1, freeSpaceRemaining])
                            #we've added a new free block after the front and end index so end index needs to increment  
                            self.endSegmentIdx += 1    
                        nextSegFromEnd = None
                        return True
        return False


    def performDefragmentation(self):
        while self.endSegmentIdx > 0:
            self.moveNextFileToFirstFreeSpace()             


with open('input/Day09.txt', 'r') as file:
    line = file.readline().replace('\n', '')

checkSums = [0, 0]

##############
# Fragment
##############
fragmentor = Fragmentor(line)
fragmentor.performFragmentation()
checkSums[0] = fragmentor.calcChecksum()
print("Part 1 fragmented checksum: {0}".format(checkSums[0]))

##############
# Defragment
##############
defragmentor = Defragmentor(line)
defragmentor.buildAllDiskBlocks()
defragmentor.performDefragmentation()

checkSums[1] = defragmentor.calcChecksum()
print("Part 2 defragmented checksum: {0}".format(checkSums[1]))
