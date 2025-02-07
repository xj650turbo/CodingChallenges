import heapq
class PriorityQueue:
    def __init__(self, nodeList=None, nodePriorityFunction = None):
        self.pqueue = [] if nodeList == None else nodeList
    
    def __bool__(self):
        return self.pqueue == True
        
    def push(self, node):
        heapq.heappush(self.pqueue, node)

    def pop(self, node):
        return heapq.heappop(self.pqueue, node)