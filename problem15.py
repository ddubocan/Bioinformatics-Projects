## Name: Danilo Dubocanin
##Purpose: Given an Adjacency List with Edge Weight, with a source and sink node,
##          generate the Length of the Longest possible path and return the longest
##          possible path.

import sys
import collections
import copy

class LongestPathInDAG(object):
    '''Generate the length and the path of the longest path in a DAG. Read in the adjacency graph
        with weight edge specified. Clean up the graph by removing nodes that cannot be in the
        path between the source node and sink node. Topologically order the cleaned-up graph. Use the
        topological ordering to find the length of the longest graph. Use the longest length to find the
        longest path.'''

    def __init__(self, sequenceFile):
        '''Initialize the class. Call required functions. Print output.'''
        sourceNode, sinkNode, dAG, inDegrees = self.reader(sequenceFile)
        #generate the source node, sink node, DAG, and inDegrees by reading in the file
        dAG, cleandInDegree= self.cleanr(sourceNode, sinkNode, dAG, inDegrees)
        #clean up the input data by removing all nodes that cannot be incorporated into a path
        #between the source node and the sink node
        topoDAG = self.topologicalOrdering(sourceNode, cleandInDegree, dAG, sinkNode)
        #topographically order the DAG
        scoreDict = self.lengthOfLongestPath(sourceNode, topoDAG, sinkNode, cleandInDegree)
        #score every node in the with its highest possible score, the score of the sinkNode is the
        #length of the Longest Path
        path = self.thePath(topoDAG, sinkNode, scoreDict)
        #using the score dictionary and topographically ordered DAG calculate the longest path
        print(scoreDict[sinkNode])
        print(*path, sep=('->'))

    def reader(self, sequenceFile):
        '''Read in source node, sink node, and adjacency graph with weights. Store source
            node and sink node as individual variables. Store adjacency graph as dictionary.'''

        sourceNode = sequenceFile.readline()
        sourceNode = sourceNode.strip()
        sourceNode = int(sourceNode)
        #reads in source node, strips of new line character, and sets as integer
        sinkNode = sequenceFile.readline()
        sinkNode = sinkNode.strip()
        sinkNode = int(sinkNode)
        #reads in sink node, strips line of new line character, and sets as integer
        dAG = {}
        #input DAG saved as a dictionary where the structure is node = [(edge, weight)]
        #node key can have multiple edges and weights
        inDegrees = {}
        #inDegrees is a dictionary that keeps track of the in-degree of each node
        #structure of inDegrees is node = key, and value is an integer representing
        #in-degree
        for line in sequenceFile.readlines():
            #read in the DAG
            line.strip()
            nums = [num.strip() for num in line.split('->')]
            #strip of new line character and remove arrow
            edgeAndWeightrough = nums[1]
            edgeAndWeightfinal = [num.strip() for num in edgeAndWeightrough.split(':')]
            #remove colon between the out-edge and the weight of that edge
            key = int(nums[0])
            #the node is in the 0th position of the line when it is read in as a list, and
            #will be used as the key in dAG dictionary
            value = (int(edgeAndWeightfinal[0]), int(edgeAndWeightfinal[1]))
            #the value for the DAG is an edge, and its weight, stored together as a tuple (edge, weight)
            if value[0] == sourceNode:
                continue
            #value[0] is equal to the outedge, if the outedge is leading to the source node we do not want it in our DAG
            #because we are searching for an acyclic path and thus one that has no edges leading into the source node
            #use 'continue' so no edges leading to source are in the DAG dictionary and then set the source node in the
            # in-degree dictionary to 0
            if value[0] not in inDegrees:
                inDegrees[value[0]] = 1
            else:
                inDegrees[value[0]] +=1
            #the edge in in DAG represents a node with an edge going into it, thus
            #for every edge going into a node we increase its in-degree in the in-degree
            #dictionary. If it is not in the dictionary we create a new entry where the
            #in-degree is 1
            if key not in dAG:
                dAG[key] = [value]
            else:
                dAG[key].append(value)
            #if the key is not in DAG dictionary, create a new entry with its associated value.
            # If the key already in the DAG
        for key in dAG:
            if key not in inDegrees:
                inDegrees[key] = 0
        #if the key is in the DAG dictionary but not in indegrees at this point, then there are no nodes
        #leading into it and thus the in-degrees are set to 0
        inDegrees[sourceNode] = 0
        #we never add any nodes with outedges
        return sourceNode, sinkNode, dAG, inDegrees

    def topologicalOrdering(self, sourceNode, cleandInDegree, dAG, sinkNode): #Adapted from textbook
        '''Topologically order an input graph. Generate a list of candidate nodes with
            0 in-degree. Update list as you go. Iterate through candidates and if they have
            in-degree = 0, append them to a list. Iterate through list, and add them to an ordered
            dictionary.'''
        #Adapted this code from the textbook(Compeau and Pevzner)
        candidates = [sourceNode]
        #create a list of candidate nodes(nodes with 0 in-degrees). The first node in this list of candidates would be
        #the source node because it is the only node with 0 in-degrees. Once you iterate past a node in the candidates
        #list remove it from the list. Any new nodes with 0 in-degrees need to be added to the candidates list
        topoList = []
        #generates a list of nodes, which are appended in the order they are traversed. Use this list later to generate
        #an orderedDict
        inDegrees2 = copy.deepcopy(cleandInDegree)
        #make a deep copy of the cleaned up in Degree dictionary to make edits too. Make a deep copy so the original dictionary
        #is not altered. As we traverse the graph we will subtract in-degrees from the copied(inDegrees2) dictionary.
        while candidates != []:
            node = candidates[0]
            topoList.append(node)
            candidates.remove(node)
        #while candidates is not empty, arbitrarily pick a node to inspect out edges. In this case we will just pick the
        #first one. Append the node to the topographic list. Then remove the node from candidates because we have traversed
        #it.
            if node == sinkNode:
                break
            #if the node is the sink node(end) then we've topographically traversed the DAG.
            if node not in dAG:
                continue
            #if the node has no out edges it wont be in dAG dictionary, so skip it.
            for edge in dAG[node]:
                newNode = edge[0]
                inDegrees2[newNode] -= 1
                if inDegrees2[newNode] == 0:
                     candidates.append(newNode)
            #We need to look at the out-going edges from every node. We are removing the current node so we need to
            #subtract 1 in-degree each of the next nodes. If the out-going edges now lead to nodes with an in-degree of
            #0, append these nodes to the candidates list
        topoDAG = collections.OrderedDict()
        for node in topoList:
            if node == sinkNode:
                break
            if node not in dAG:
                continue
            value = dAG[node]
            topoDAG[node] = value
        #iterate through the topographically ordered list and append the node(as a key) and edges and weights(as a vvalue)
        #to the orderedDict
        return topoDAG

    def lengthOfLongestPath(self, sourceNode, topoDAG, sinkNode, cleandInDegree):
        '''Calculate length of longest path. Iterate through topographically ordered graph,
            calculate highest score at that position based of highest score at prior node.
            Return a dictionary of scores.'''
        scoreDict = {} #key = node, value = [score]
        scoreDict[sourceNode] = 0
        #initialize a dictionary to keep track of the highest score for each node
        #the sourceNode will have a score of 0 because it if the first node in our path
        for node in topoDAG:
            for edgeAndWeight in topoDAG[node]:
                edge = edgeAndWeight[0]
                weight = edgeAndWeight[1]
                if edge in scoreDict:
                    if scoreDict[edge] < scoreDict[node] + weight:
                        scoreDict[edge] = scoreDict[node] + weight
                else:
                    scoreDict[edge] = scoreDict[node] + weight
        #Iterate through the topographic DAG (a topographically ordered orderedDict) and traverse each edge from every node.
        #If the node at the terminal end of the edge already has a score in score dictionary, check to see if traversing the edge
        #from the current node generates a higher score. Assign the higher score to the node value in scoreDict.
        #if there is no entry for that particular node in scoreDict. Then the calculated score is its value.
        #this is essentially just dynamic programming, for each edge you use the highest score of the prior node added
        #to the weight of the edge to the next node to calculate that next node's score
        return scoreDict

    def thePath(self, topoDAG, sinkNode, scoreDict):
        '''Generate Longest Path in DAG. Iterate through a reversed topologically ordered dictionary. Check if node
            contains an edge to the latest node in the path. If it does, check that the highest score of the latest node in the
            path originated from the highest score of the current node in the topologically ordere data structure. It it did, add
            node to path.'''
        path = [sinkNode]
        #we are backtracking through our graph to find the path, so the first node in the path will be the sink node
        for node in reversed(topoDAG):
            backTrackNode = path[0]
        #iterate through our reversed topographical orderedDict(because we are backtracking), set the current node
        #as the most recent node in the path(located at position 0)
            for v in topoDAG[node]:
                if backTrackNode == v[0]:
                    currentscore = scoreDict[backTrackNode]
                    if currentscore - v[1] == scoreDict[node]:
                        path = [node] + path
            #for each node in topoDAG, check its out going edges to see if it leads to backTrackNode. If it does, check
            #to see that the score of the backTrackNode - the weight of the edge = the score of the node. If it does,
            #than this is the node that needs to be traversed in the path. Add this node to the front of the path.
        return path

    def cleanr(self, sourceNode, sinkNode, dAG, inDegrees):#problem in cleanr
        '''Find all nodes that cannot be included in a path between the source and sink node, and
            remove these nodes from all data structures. Use in-degree data structure to select
            all nodes other than the source node with an in-Degree of zero. Remove these nodes and their
            edges. Update in-degree data structure, remove nodes with updated in-degree of zero.
            Continue until no nodes with zero in-degree (except source node).'''
        badStarts = []
        #nodes with 0 in-degree that are not the source-node should not be included
        #in the DAG because they cannot be included in the longest possible path
        #that includes our specified source node
        badNodes = []
        #as we traverse the graph from nodes in badStarts, nodes with 0 in-degree
        #if we remove bad-starts are nodes that could not be included in the path
        #so they are added to badnodes. These nodes will be removed from our graph later.
        for node in inDegrees:
            if node == sourceNode:
                continue
            if inDegrees[node] == 0:
                badStarts.append(node)
                badNodes.append(node)
        #add nodes with 0 in-degrees that are not the source node to badStarts
        while badStarts != []:
        #while there is a node in badStarts keep on iterating
            for node in badStarts:
                if node not in dAG:
                    badNodes.remove(node)
                    badStarts.remove(node)
                    continue
        #if node had an incoming edges but no out going edges they would not be in our dAG dictionary
        #so we remove them from badNodes
                for value in dAG[node]:
                    nextNode = value[0]
                    inDegrees[nextNode] -= 1
                    if inDegrees[nextNode] == 0:
                        badStarts.append(nextNode)
                        badNodes.append(nextNode)
                badStarts.remove(node)
        #As we traverse the graph from badStarts, Nodes that have 0 in-degree if we remove badStart
        #are added to badstarts and badnodes
        for node in badNodes:
            del dAG[node]
        #remove the bad nodes from the DAG dictionary
        cleandInDegree = {} #key = node value = in degree
        for node in dAG:
            for edge in dAG[node]:
                nxtNode = edge[0]
                if nxtNode not in cleandInDegree:
                    cleandInDegree[nxtNode] = 1
                else:
                    cleandInDegree[nxtNode] += 1
        cleandInDegree[sourceNode] = 0
        #Generate a new inDegree dictionary when all the bad nodes are removed
        return dAG, cleandInDegree

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program. Take in input file from stdin. Call Reconstructor class on the input file.'''
    sequenceFile = sys.stdin
    LongestPathInDAG(sequenceFile)

if __name__ == "__main__":
    main()