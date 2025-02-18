import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import heapq

class Graph:
    def __init__(self):
        self.graph = None
        self.startNode = None
        self.endNode = None
        self.costFunction = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


    # build a graph. Arguments:
    # - map: BaseMap with an internal board representing a map from which graph is built
    # - moves: allowed moves
    # - start - start int/char which will become the start node of the graph 
    # - end - end int/char which will become the end node of the graph 
    # - obstacles - a list of obstacle ints/chars which are impassable withing the board 
    # - costFunction: a cost function from previous node to current node
    def buildGraphFromMap(self, map, moves, start = 'S', end = 'E', obstacles = ['#'], costFunction = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])):
        if self.costFunction is None:
            self.costFunction = costFunction
        self.graph = nx.Graph()
        # add all nodes that are not walls
        for row in range(map.board.shape[0]):
            for col in range(map.board.shape[1]):
                pos = (row, col)
                cell = str(map.board[row, col])
                node = (pos, cell)
                if cell not in obstacles:
                    #find all neighbours around this position
                    for toNeighbour in moves.moveCommands:
                        neighbourPos = tuple(moves.move(toNeighbour, pos))
                        neighbourPos = tuple((int(x) for x in neighbourPos))
                        if map.inBounds(neighbourPos):
                            neighbourCell = str(map.board[neighbourPos[0], neighbourPos[1]])
                            neighbourNode = (neighbourPos, neighbourCell)
                            if neighbourCell not in obstacles:
                                if pos not in self.graph.nodes:
                                    self.graph.add_node(node)
                                    if cell == start:
                                            self.startNode = node
                                    if cell == end:
                                            self.endNode = node
                                if neighbourPos not in self.graph.nodes:
                                    self.graph.add_node(neighbourNode)
                                    self.graph.add_edge(node, neighbourNode, weight=costFunction(pos, neighbourPos))


    # build a Directed graph. Arguments:
    # - map: a BaseMap object with an internal board representing a map from which graph is built
    # - moves: a Moves objests of allowed moves
    # - start - start int/char which will become the start node of the graph 
    # - end - end int/char which will become the end node of the graph 
    # - obstacles - a list of obstacle ints/chars which are impassable withing the board 
    def buildDirGraphFromMap(self, map, moves, start = 'S', end = 'E', obstacles = ['#']):
        self.graph = nx.DiGraph()
        # add all nodes that are not walls
        for row in range(map.board.shape[0]):
            for col in range(map.board.shape[1]):
                pos = (row, col)
                cell = str(map.board[row, col])
                if cell not in obstacles:
                    nodes = []
                    #find all directional neighbours around this position
                    neighbourNodes = []
                    for toNeighbour in moves.moveCommands:
                        neighbourPos = tuple(moves.move(toNeighbour, pos))
                        neighbourPos = tuple((int(x) for x in neighbourPos))
                        if map.inBounds(neighbourPos):
                            neighbourCell = str(map.board[neighbourPos[0], neighbourPos[1]])
                            neighbourNode = (neighbourPos, neighbourCell, toNeighbour)
                            # reverse direction to be neighbour node --> this node
                            fromNeighbour = moves.turn(toNeighbour, 180)[0]
                            node = (pos, cell, fromNeighbour)
                            if neighbourCell not in obstacles:
                                neighbourNodes.append(neighbourNode)
                                nodes.append(node)
                                if node not in self.graph.nodes:
                                    self.graph.add_node(node)
                                if neighbourNode not in self.graph.nodes:
                                    self.graph.add_node(neighbourNode)
                            else:
                                if cell == start:
                                    nodes.append(node)

                    if len(nodes) > 0 and len(neighbourNodes) > 0:
                        for node in nodes:
                            nodeFromDir = node[2]
                            # ignore neighbour in reverse direction, i.e. where we came from
                            ignoreNeighbourInDir = moves.turn(nodeFromDir, 180)[0]
                            for neighbourNode in neighbourNodes:
                                neighbourFromDir = neighbourNode[2]
                                if node[1] != end and ignoreNeighbourInDir != neighbourFromDir:
                                    cost = 1 if nodeFromDir == neighbourFromDir else 1001
                                    self.graph.add_edge(node, neighbourNode, weight=cost)

        startNodes = [node for node in self.graph.nodes if node[1] == start and node[2] == '>']
        if len(startNodes) > 0:
            self.startNode = startNodes[0]

        #we only want to have one end node, so merge all directional end nodes into 1
        endNodes = [node for node in self.graph.nodes if node[1] == end]
        if len(endNodes) > 0:
            for i in range(1, len(endNodes)):
                self.graph = nx.contracted_nodes(self.graph, endNodes[0], endNodes[i], self_loops=False)            
            self.endNode = endNodes[0]

    ###############################################################################
    # Below functions use cusom implementation on top of networkx graph structure
    ###############################################################################

    # Run Dzikstra to return the least cost. Arguments:
    # - startNode: a graph node from which to start 
    # - endNode: a graph node at which to end
    # - costFunction: a cost function from previous node to current node
    def dzikstraShortestPath(self, startNode, endNode, costFunction = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])):
        costAtNode = {node : float('inf') for node in self.graph.nodes} # {node: leastCost)}
        costAtNode[startNode] = 0     # set cost for the start node to 0
        priQueue = [(0, startNode)]

        while priQueue:
            cost, currNode = heapq.heappop(priQueue)
            if cost > costAtNode[currNode]:
                continue

            for nextNode in self.graph.neighbors(currNode):
                nextCost = cost + costFunction(currNode[0], nextNode[0])
                if nextNode == endNode:
                    return nextCost
                if nextCost < costAtNode[nextNode]:
                    costAtNode[nextNode] = nextCost
                    heapq.heappush(priQueue, (nextCost, nextNode))
        return None


    # Run Dzikstra to return the least cost and all least cost paths. Arguments:
    # - startNode: a graph node from which to start 
    # - endNode: a graph node at which to end
    # - costFunction: a cost function from previous node to current node
    def dzikstraAllLeastCostPaths(self, startNode, endNode, costFunction = lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])):
        costAndPaths = {node : [float('inf'), []] for node in self.graph.nodes} # {node: (cost, shortestPathsArray)}
        costAndPaths[startNode][0] = 0     # set cost for the start node to 0
        costAndPaths[startNode][1] = [[startNode]]    # set paths for the start node to []
        priQueue = [(0, startNode)]

        while priQueue:
            cost, currNode = heapq.heappop(priQueue)
            if cost > costAndPaths[currNode][0]:
                continue
            if currNode == endNode:
                break
            
            for nextNode in self.graph.neighbors(currNode):
                nextCost = cost + costFunction(currNode[0], nextNode[0])
                if nextCost <= costAndPaths[nextNode][0]:
                    costAndPaths[nextNode][0] = nextCost
                    for prevShortestPath in costAndPaths[currNode][1]:
                        shortestPathPlusCurr = prevShortestPath + [nextNode]
                        if shortestPathPlusCurr not in costAndPaths[nextNode][1]:
                            costAndPaths[nextNode][1].append(shortestPathPlusCurr)
                    heapq.heappush(priQueue, (nextCost, nextNode))
        return costAndPaths


    #####################################################################
    # Below functions use networkx algorithms
    #####################################################################

    # finds shortest path length
    def onlyShortestSimplePaths(self):
        shortestSimpleGen = nx.shortest_simple_paths(self.graph, self.startNode, self.endNode, weight='weight')
        shortestSimple = next(shortestSimpleGen)
        shortestSimpleLen = len(shortestSimple)
        yield shortestSimple

        for path in shortestSimpleGen:
            if len(path) == shortestSimpleLen:
                yield path
            else:
                break

    def hasPath(self):
        return nx.has_path(self.graph, self.startNode, self.endNode)

    # finds shortest path length
    def shortestPathLength(self):
        return nx.shortest_path_length(self.graph, self.startNode, self.endNode, weight='weight')

    # finds all shortest paths
    def allShortestPaths(self):
        pathsGenerator = nx.all_shortest_paths(self.graph, self.startNode, self.endNode, weight='weight')
        return pathsGenerator 

    # finds all simple paths
    def allSimplePaths(self):
        pathsGenerator = nx.all_simple_paths(self.graph, self.startNode, self.endNode)
        return pathsGenerator 


    def plotGraph(self):
        nodeColorMap = {
            'S': "lightgreen",
            'E': "red",
            '.': "lightblue"
        }
        # Draw the graph with spring layout (Fruchterman-Reingold force-directed algorithm)
        #pos = nx.spring_layout(self.graph, weight='weight', seed=11, k=0.3)  # Use a layout for better visualization

        # Draw the graph using graphviz with custom layout
        # "dot": Default layout, good for basic graphs. 
        #"neato": Force-directed layout, often preferred for complex graphs. 
        #"twopi": Radial layout, useful for visualizing hierarchical relationships 
        #"fdp": Force-directed layout with improved aesthetics 
        #"sfdp": Similar to fdp but with additional features 
        #"circo": Circular layout  
        pos = nx.nx_pydot.graphviz_layout(self.graph, prog='sfdp')
        weights = nx.get_edge_attributes(self.graph, 'weight')
        nodeColors = [nodeColorMap[node[1]] for node in self.graph]

        #draw the graph itself
        nx.draw(self.graph, pos=pos, with_labels=True, node_color=nodeColors, node_size=200, arrows=True)

        #draw labels
        nx.draw_networkx_edge_labels(self.graph, pos=pos, edge_labels=weights)
        plt.show()

