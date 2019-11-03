## Name: Danilo Dubocanin
##Purpose: Given an Adjacency List with Edge Weight, with a source and sink node,
##          generate the Length of the Longest possible path and return the longest
##          possible path.
import sys
from operator import itemgetter
import math
import collections

import copy

class LongestPathInDAG(object):
    def __init__(self, sequenceFile):
        sourceNode, sinkNode, dAG, inDegrees = self.reader(sequenceFile)
        dAG, cleandInDegree= self.cleanr(sourceNode, sinkNode, dAG, inDegrees)
        topoList, topoDAG = self.topologicalOrdering(sourceNode, cleandInDegree, dAG, sinkNode)
        scoreDict = self.lengthOfLongestPath(sourceNode, topoDAG, sinkNode, cleandInDegree)
        path = self.thePath(topoDAG, sinkNode, scoreDict)
        print(scoreDict[sinkNode])
        print(*path, sep=('->'))

    def reader(self, sequenceFile):
        #generate a dictionary that keeps count of the number of in-edges a node has
        sourceNode = sequenceFile.readline()
        sourceNode = sourceNode.strip()
        sourceNode = int(sourceNode)
        sinkNode = sequenceFile.readline()
        sinkNode = sinkNode.strip()
        sinkNode = int(sinkNode)
        dAG = {}
        inDegrees = {}
        for line in sequenceFile.readlines():
            line.strip()
            nums = [num.strip() for num in line.split('->')]
            edgeAndWeightrough = nums[1]
            edgeAndWeightfinal = [num.strip() for num in edgeAndWeightrough.split(':')]
            key = int(nums[0])
            value = (int(edgeAndWeightfinal[0]), int(edgeAndWeightfinal[1])) #structure of dAG dictionary is key = node, value = [(edge, weight)]
            if value[0] not in inDegrees:
                inDegrees[value[0]] = 1
            else:
                inDegrees[value[0]] +=1
            if key not in dAG:
                dAG[key] = [value]
            else:
                dAG[key].append(value)
        for key in dAG:
            if key not in inDegrees:
                inDegrees[key] = 0
        return sourceNode, sinkNode, dAG, inDegrees

    def topologicalOrdering(self, sourceNode, cleandInDegree, dAG, sinkNode):
        candidates = [sourceNode]
        topoList = []
        inDegrees2 = copy.deepcopy(cleandInDegree)
        while candidates != []:
            node = candidates[0]
            topoList.append(node)
            candidates.remove(node)
            if node == sinkNode:
                break
            if node not in dAG:
                continue
            for edge in dAG[node]:
                newNode = edge[0]
                inDegrees2[newNode] -= 1
                if inDegrees2[newNode] == 0:
                     candidates.append(newNode)
        topoDAG = collections.OrderedDict()
        for node in topoList:
            if node == sinkNode:
                break
            if node not in dAG:
                continue
            value = dAG[node]
            topoDAG[node] = value
        return topoList, topoDAG

    def lengthOfLongestPath(self, sourceNode, topoDAG, sinkNode, cleandInDegree):
        '''Calculate length of longest path. Iterate through topographically ordered graph,
            calculate highest score at that position based of highest score at prior node.
            Return a dictionary of scores.'''
        scoreDict = {} #key = node, value = [score]
        scoreDict[sourceNode] = 0
        #topoDAG is ordered dictionary where key is the node, value is [edge, weight]
        for node in topoDAG:
            for edgeAndWeight in topoDAG[node]:
                edge = edgeAndWeight[0]
                weight = edgeAndWeight[1]
                if edge in scoreDict:
                    if scoreDict[edge] < scoreDict[node] + weight:
                        scoreDict[edge] = scoreDict[node] + weight
                else:
                    scoreDict[edge] = scoreDict[node] + weight
        return scoreDict

    def thePath(self, topoDAG, sinkNode, scoreDict):
        '''Generate Longest Path in DAG. Iterate through a reversed topologically ordered dictionary. Check if node
            contains an edge to the latest node in the path. If it does, check that the highest score of the latest node in the
            path originated from the highest score of the current node in the topologically ordere data structure. It it did, add
            node to path.'''
        path = [sinkNode]
        for node in reversed(topoDAG):
            backTrackNode = path[0]
            for v in topoDAG[node]:
                if backTrackNode == v[0]:
                    currentscore = scoreDict[backTrackNode]
                    if currentscore - v[1] == scoreDict[node]:
                        path = [node] + path
                    else:
                        continue
                else:
                    continue
        return path

    def cleanr(self, sourceNode, sinkNode, dAG, inDegrees):#problem in cleanr
        '''Find all nodes that cannot be included in a path between the source and sink node, and
            remove these nodes from all data structures. Use in-degree data structure to select
            all nodes other than the source node with an in-Degree of zero. Remove these nodes and their
            edges. Update in-degree data structure, remove nodes with updated in-degree of zero.
            Continue until no nodes with zero in-degree (except source node).'''
        badStarts = []  # none-source starts
        badNodes = []
        for node in inDegrees:
            if node == sourceNode:
                continue
            if inDegrees[node] == 0:
                badStarts.append(node)
                badNodes.append(node)
        while badStarts != []:
            for node in badStarts:
                if node not in dAG:
                    badNodes.remove(node)
                    badStarts.remove(node)
                    continue
                for value in dAG[node]:
                    nextNode = value[0]
                    inDegrees[nextNode] -= 1
                    if inDegrees[nextNode] == 0:
                        badStarts.append(nextNode)
                        badNodes.append(nextNode)
                badStarts.remove(node)
        for node in badNodes:
            del dAG[node]
        cleandInDegree = {} #key = node value = in degree
        for node in dAG:
            for edge in dAG[node]:
                nxtNode = edge[0]
                if nxtNode not in cleandInDegree:
                    cleandInDegree[nxtNode] = 1
                else:
                    cleandInDegree[nxtNode] += 1
        cleandInDegree[sourceNode] = 0
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