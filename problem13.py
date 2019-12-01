## Name: Danilo Dubocanin
## Worked With: Kavya Aswadhati, Alex Zee
## Prupose: Given a directed graph, represented as an adjacency list, that contains a Eulerian Path, find and
##          output the Eulerian path in this graph.

import sys
import random
import copy
class EulerianPath(object):
    def __init__(self, sequenceFile):
        '''Read in file to generate the adjacency list as a dictionary, where keys are nodes and values are outgoing-edges,
            generate a degree dictionary to compare each nodes in degree and out degree, and find the Eulerian path length.
            Utilize the degree dictionary to find the start and end of the Eulerian Path. Call a Eulerian path function
            to use the input(graph) dictionary, path length, start node, and end node to generate a Eulerian path.
            Print the Eulerian path.'''
        inputDict, degreeDict, pathLength, outlier = self.adjacencyListReader(sequenceFile) #values of dict are in list form
        start, end = self.startFinder(degreeDict, outlier)
        inputDict[end].append(start)
        #cirulatize the path to make the Eularian Path into a Eularian Cycle. All nodes have an even indegree and outdegree
        self.availableEdges=[]
        self.pathSize = 0
        #size of the path I have currently traversed
        path = self.eulerianRoute(inputDict, pathLength, start, end)
        i = 0
        for element1, element2 in zip(path, path[1:]):
            #repurposed this zip function from stackoverlow. Purpose of this zip function is to analyze a node and
            #the node after it. When the end node has an edge leading the start node this indicates the end of the path
            #then you splice the list and add the latter part(containing the start at the front)
            # in front of the first to generate the proper Eulerian Path
            if element1 == end and element2 == start:
                path = path[i+1:] + path[1:i+1]
            i +=1


        print(*path, sep='->')
        #repurposed this print statement from stackoverflow. prints every element of path list with an arrow between them

    def adjacencyListReader(self, sequenceFile):
        '''Read in the input File. Generate an input Dictionary containing Node: [Outgoing Edges]. Generate a
            degree dictionary specifying each node's in-degree and out-degree. Find the path length. Store any node which
            does not contain equal in- and out-degrees.'''
        end = ''
        pathLength = 0
        #keep track of the current path length, at the beginning it is 0
        inputDict = {}#structured as node: [all edges]
        degreeDict = {} #dictionary is structured as number node as key: [indegree, outdegree]
        for path in sequenceFile.readlines():
            path = path.strip()
            nums = [num.strip() for num in path.split('->')]
            #read through eack line in the file and strip it of new line characters and split it into the node
            #and the outedges (head = outedges)
            head = nums[1]
            node = int(nums[0])
            degreeDict[int(nums[0])] = [0,0]
            heads = [value.strip() for value in head.split(',')]
            #generate a list of all the outedges and make them integers
            heads = [int(value) for value in heads]
            inputDict[node] = heads
            #set the node as the key and all its outedges(as a list) as the value)
            degreeDict[node][1] = len(heads)
            #the length of the heads variable is the number of outedges. This is stored at the 1 position of the value list
        outlier = 'none'
        for node in inputDict:
            for outedge in inputDict[node]:
                if outedge not in inputDict:
                    #iterate through all the nodes and then iteratre through their edges
                    #if one of the nodes that the edges lead too is not in the inputDict then that means it is an end node
                    #that leads to no other nodes, mark this as an outlier
                    outlier = outedge #the outlier is head tail is node
                    degreeDict[outlier] = [1,0]
                degreeDict[outedge][0] += 1
            pathLength += len(inputDict[node])
            #the pathlength is equal to the number of outedges each node has
        inputDict[outlier] = []

        return inputDict, degreeDict, pathLength, outlier


    def startFinder(self, degreeDict, outlier):
        '''Iterate through dictionary containing Nodes and their in-/out-degree, and compare in- vs out- degree.
            If more out- than in- degrees this indicates start. If more in- than out-degrees, indicate end of Eulerian
            path. Set end equal to the outlier, if it was not in the input Dictionary than it has no out-degrees. '''
        for node in degreeDict:
            if degreeDict[node][0] < degreeDict[node][1]:
                start = node
            #if the outdegree is greater than the indegree than that indicates the starting node
        end = outlier
        #the outlier had no out-degrees so in-degree>out-degree and therefore must be end of path
        return start, end

    def eulerianRoute(self, inputDict, pathLength, start, end):
        '''Copy input Dictionary into a path dictionary which will be changed as path is generated.
            Iterate through nodes with available edges by calling cycler function until the path size is equal to the
            true path length.Pick a random position in the path with available sequences if last position on current
            path has no more available nodes. Cycle through this subpath and splice it into current path list after
            the position in which it was started.'''
        self.pathDict = copy.deepcopy(inputDict)
        #the pathDict will be an updated version of inputDict(graph). Need to make a copy in order for the inputDict to not be changed
        for node in self.pathDict:
            self.availableEdges.append(node)
            #populate the availableEdges list
        currentPath = [start]  # the start of the current path is the start node
        while self.pathSize < pathLength:  # if pathsize is smaller than pathlength then route needs to be traversed
            if self.pathDict[currentPath[-1]] == []:
                # if no available edges at that node pick a random node in the current path
                savedPos = random.randint(0, len(currentPath) - 1)
                if currentPath[savedPos] not in self.availableEdges:
                    continue
                    #if the randomly selected node has no available edges than pick another
                currentNode = currentPath[savedPos]
                subcycle = [currentNode]  # the subcycle starts with the current node
                subcycle = self.cycler(subcycle)
                #start a new subpath from this randomly selected node
                currentPath = currentPath[0:savedPos + 1] + subcycle[1:] + currentPath[savedPos + 1:]
                #splice sub-cycle back into main cycle
            else:
                currentPath = self.cycler(currentPath)
                #just cycle through the path if there are available edges
        return currentPath

    def cycler(self, currentPath):
        '''Traverse the edges of path and append the nodes in order to a list. While the most recent node has an available
            edge to traverse continue traversing. Update path dictionary, available edges list, and pathsize while the loop
            continues. If multiple edges are available to traverse, randomly pick one.'''
        outEdges = self.pathDict[currentPath[-1]]
        #the available edges are the out edges of the latest node in the path
        while outEdges != []:
            #if there are available edges, traverse them
            chosenNode = outEdges[0]
            if len(outEdges) > 1:
                chosenNode = outEdges[random.randint(0, len(outEdges) - 1)]
            #randomly pick an edge if there are multiple
            self.pathDict[currentPath[-1]].remove(chosenNode)
            if len(outEdges) == 0:
                self.availableEdges.remove(currentPath[-1])
            #remove edge from path dictionary and if there are no more edges remove the node from available edges
            currentPath.append(chosenNode)
            #add the node to current path
            outEdges = self.pathDict[currentPath[-1]]
            self.pathSize += 1
            #find the new outedges for the next iteration, and add to the path size
        return currentPath

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program.'''
    sequenceFile = sys.stdin
    EulerianPath(sequenceFile)

if __name__ == "__main__":
    main()