## Name: Danilo Dubocanin
## Worked With: Kavya Aswadhati, Alex Zee
##Purpose:  Given an integer k followed by a list of k-mer patterns, reconstruct the DNA sequence by representing
##          the kmers as a De Brujin Graph and finding the Eulerian path through the graph.


import sys
import random
import copy
from problem9 import SequenceGenerator
from problem11 import DeBruijnGraphFromString

class Reconstructor(object):
    '''Generate a sequence from a text file of kmers. Generate a de Brujin Graph consisting of Nodes where the edges are
        the overlap between the nodes. Find the Eulerian path through this De Brujin Graph, and use this to create
        a sequence.'''
    def __init__(self, sequenceFile):
        ''' Initialize the class. use SequenceGenerator.reader from problem9 to find the Kmers. Generate the De Bruijn
            Graph using DeBruijnGraphFromString.linkageGraph from problem11. Functions within the Reconstructor class to
            construct a eulerian path through the De Brujin graph of Kmers.'''
        k = sequenceFile.readline()
        k = k.strip()
        k = int(k)
        #first line in the file is a kmer, save as an integer
        kmers = SequenceGenerator.reader(self, sequenceFile)
        #generate a list of kmers
        DeBrujinGraph = DeBruijnGraphFromString.linkageGraph(self, k, kmers)
        #generate DeBrujin Graph
        graphForPath = {}
        for edge in DeBrujinGraph:
            graphForPath[edge] = [','.join(DeBrujinGraph[edge])]
        #turn De Brujin Graph in a data structure form more appropriate for this problem(

        graphForPath, degreeDict, pathLength, outlier = self.graphUnderstander(graphForPath)
        #generate other variables necessary for path construction, such as looking at the indegree and out degree per
        #kmer, path length, and finding the outlier kmer(to find end)

        start, end = self.startFinder(degreeDict, outlier)
        #find the start and then end
        graphForPath[end].append(start)
        #circularize path
        self.availableEdges=[]
        self.pathSize = 0
        path = self.eulerianRoute(graphForPath, pathLength, start, end)
        #find the eulerian route
        self.outputter(path, end, start)
        #formatting output for printing

    def outputter(self, path, end, start):
        '''Find start and end of path. Iterate across path and when end occurs immediately before start it indicates
            that that is the true start. Generate the final sequence using the path and each node.'''
        i = 0
        for element1, element2 in zip(path, path[1:]):#stack
            if element1 == end and element2 == start:
                path = path[i+1:] + path[1:i+1]
            i +=1
            #searches for position where end -> start, sets this start as the true start of path and the end as the end
        output = []
        x= 0
        for kmer in path:
            if x == 0:
                output.append(kmer)
            else:
                output.append(kmer[-1])
            x+=1
        #generates sequence from the path by traversing the path and just adding the nonoverlapping portion
        output = ''.join(output)
        print(output)
        #need to accurately find beginning and end in this sequence

    def graphUnderstander(self, graphForPath):
        '''Generate an input Dictionary (graphForPath) containing Node: [Outgoing Edges]. Generate a
            degree dictionary specifying each node's in-degree and out-degree. Find the path length. Store any node which
            does not contain equal in- and out-degrees.'''
        pathLength = 0
        degreeDict = {} #dictionary is structured as number node as key: indegree, outdegree
        for node in graphForPath:
            degreeDict[node] = [0,0]
            degreeDict[node][1] = len(graphForPath[node])
            #populate the degree dictionary and the out degree is equivalent to the edges associated with each node
            #at input
        outlier = 'none'
        for node in graphForPath:
            for outedge in graphForPath[node]:
                if outedge not in graphForPath:
                    outlier = outedge #the outlier is head tail is node
                    degreeDict[outedge] = [1,0]
                    continue
                degreeDict[outedge][0] += 1
            pathLength += len(graphForPath[node])
        #generate the in degree value of the degree dictionary by counting the number of times another node as an
        #outedge to that specific node, if we come across the end, which may have not been in the input dictionary,
        #we create a key for that outlier. While iterating we can count the number of edges and this is the pathlength
        graphForPath[outlier] = []
        #crete a key value for the outlier(end) in the graph dictionary we will use to generate the path
        return graphForPath, degreeDict, pathLength, outlier

    def startFinder(self, degreeDict, outlier):
        '''Iterate through dictionary containing Nodes and their in-/out-degree, and compare in- vs out- degree.
            If more out- than in- degrees this indicates start. If more in- than out-degrees, indicate end of Eulerian
            path. Set end equal to the outlier, if it was not in the input Dictionary than it has no out-degrees. '''
        for node in degreeDict:
            if degreeDict[node][0] < degreeDict[node][1]:
                start = node
        end = outlier
        return start, end

    def eulerianRoute(self, graphForPath, pathLength, start, end):
        '''Copy input Dictionary into a path dictionary which will be changed as path is generated.
            Iterate through nodes with available edges by calling cycler function until the path size is equal to the
            true path length.Pick a random position in the path with available sequences if last position on current
            path has no more available nodes. Cycle through this subpath and splice it into current path list after
            the position in which it was started.'''
        self.pathDict = copy.deepcopy(graphForPath)
        # the path dictionary will get updated so we have to make a copy of the original inputDict so it doesn't get changed
        for node in self.pathDict:
            self.availableEdges.append(node)
            #populate the available edges list, at the beginnning all edges are available
        currentPath = [start]  # the start of the current path is the start node
        while self.pathSize < pathLength:  # if pathsize is lower than pathlength then more route needs to be traversed
            if self.pathDict[currentPath[-1]] == []:  # if no available edges at that node, pick a random node and subcycle through it
                savedPos = random.randint(0, len(currentPath) - 1)
                if currentPath[savedPos] not in self.availableEdges:
                    continue
                currentNode = currentPath[savedPos]
                if currentNode in self.availableEdges:
                    if currentNode == end:
                        if len(self.pathDict[end]) == 1:
                            continue
                subcycle = [currentNode]  # the subcycle starts with the current node
                subcycle = self.cycler(subcycle)
                currentPath = currentPath[0:savedPos + 1] + subcycle[1:] + currentPath[savedPos + 1:]  # stitch subcycle into main path
            else:
                currentPath = self.cycler(currentPath)
        return currentPath

    def cycler(self, currentPath):
        '''Traverse the edges of path and append the nodes in order to a list. While the most recent node has an available
            edge to traverse continue traversing. Update path dictionary, available edges list, and pathsize while the loop
            continues. If multiple edges are available to traverse, randomly pick one.'''
        outEdges = self.pathDict[currentPath[-1]] #the available edges are the ones of the last node in the path
        while outEdges != []:
            #continue traversing while there are available outedges
            chosenNode = outEdges[0]
            if len(outEdges) > 1:
                chosenNode = outEdges[random.randint(0, len(outEdges) - 1)]
            self.pathDict[currentPath[-1]].remove(chosenNode)
            #if there is more than one edge, randomly pick one
            if len(outEdges) == 0:
                self.availableEdges.remove(currentPath[-1])
            #if there are no more available edges to traverse from that node, remove it from available edges
            currentPath.append(chosenNode)
            #update the path
            outEdges = self.pathDict[currentPath[-1]]
            #update the De Brujin Graph
            self.pathSize += 1
            #increase pathsize
        return currentPath

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program. Take in input file from stdin. Call Reconstructor class on the input file.'''
    sequenceFile = sys.stdin
    Reconstructor(sequenceFile)

if __name__ == "__main__":
    main()