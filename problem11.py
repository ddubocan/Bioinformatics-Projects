## Name: Danilo Dubocanin
## Worked With: Kavya Aswadhati, Alex Zee
##Purpose: Given a string and an integer k, generate a De Brujin Graph with the Kmers as nodes and Prefixes/Suffixes
##         as edges, and output as an adjacency list.

from problem8 import AllKmers
#import problem 8 to generate a dna string and the k size using the Allkmers class
import sys
#import sys to read stdin
class DeBruijnGraphFromString(object):
    '''Read in a value K and a DNA string from an input file and output the De Brujin graph of that
        K-mer size in the form of an adjacency list. Read in the file, find the Kmers, find the overlap
        between Kmers, and use this to construct De Brujin Graph.'''
    def __init__(self, sequenceFile):
        ''' Inititalize the class. Call reader function from problem8 to read in file and output K and DNA string.
            Call kmerMaker function from problem8 to generate a list of kmers from K and the DNA string.
            Use the list of kmers to generate a De Brujin Graph.'''
        k, sequenceString = AllKmers.reader(self, sequenceFile)
        #using the reader function from AllKmers, read in the sequenceFile and
        #store the k size and the dna string associated with the file
        kmers = AllKmers.kmerMaker(self, k, sequenceString)
        #using the kmerMaker function from AllKmers, use the sequenceString and k, to generate a list of kmers
        linkageGraph = self.linkageGraph(k, kmers)
        #use the linkageGraph function to generate a linkage graph/adjacency list using the list of kmers and k
        for edge in linkageGraph:
            print(edge, '->', ', '.join(linkageGraph[edge]))
        #prints every kmer of the linkage graph and the next kmer it leads too onto a new line

    def linkageGraph(self, k, kmers):
        '''Iterate through all kmers in kmer list. Generate a prefix and suffix for every kmer.
            Generate a dictionary where the prefix is the key and the suffix(s) corresponding to
            the prefix are the values. Return the graph dictionary.'''
        linkageGraph = {}
        #set linkageGraph next to an empty dictionary that will be filled
        for kmer in kmers:
            #iterate through every kmer in kmers
            prefix = kmer[:k-1]
            #generate the prefix by getting rid of the last nucleotide
            suffix = kmer[1:]
            #generate the suffix by getting rid of the first nucleotide
            if prefix not in linkageGraph:
                #if the prefix is not yet in the linkage
                linkageGraph[prefix] = [suffix]
                #set the key(prefix) to correspond to the value(suffix)
            else:
                linkageGraph[prefix].append(suffix)
                #if the prefix leads to multiple suffixes append it to the list
            linkageGraph[prefix].sort()
            #alphabetize them
        return linkageGraph

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg


def main(myCommandLine=None):
    '''Run the program.'''
    sequenceFile = sys.stdin
    DeBruijnGraphFromString(sequenceFile)

if __name__ == "__main__":
    main()