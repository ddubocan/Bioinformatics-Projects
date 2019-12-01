## Name: Danilo Dubocanin
## Worked With: Kavya Aswadhati, Alex Zee
##Purpose: Given a collection of kmers, generate an overlap graph and output it in the form of an adjacency list.
import sys
#import sys to read stdin
from problem9 import SequenceGenerator
#from problem9 import my sequenceGenerator to read in my sequenceFile and return a list of kmers
class OverlapGraph(object):
    '''Given a collection of of k-mers, generate the overlap graph for these Kmers
        and output in the form of an adjacency list. Read in file using SequenceGenerator.reader from problem9.
        Generate a dictionary of Kmer prefixes and suffixes. User prefixes and suffixes to generate overlap Graph'''
    def __init__(self, sequenceFile):
        '''Initialize the class. Call reader function from problem9 to read in file and output a
            list of kmers.Call prefixSuffixGenerator function to generate a dictionary of
            prefixes and suffixes.Use the prefixSuffixDict to generate an overlap Graph.'''

        kmers = SequenceGenerator.reader(self, sequenceFile)
        prefixSuffixDict = self.prefixSuffixGenerator(kmers)
        #generate a dictionary where the kmer is the key, and then [prefix,suffix] is the value
        graphDict = self.graphGenerator(prefixSuffixDict)
        #generate a dictionary where we will check which prefix overlaps with which suffix and thus
        #create a key:value pair where the key is the preceding kmer and value is the next upcoming kmer
        for kmer in graphDict:
            print(graphDict[kmer][0], '->', kmer)
        #print statement that prints every key/value pair in the graphDict with an arrow between them,
        #the value is printed first because the suffix of a kmer would be equal to the prefix
        #of the next kmer in a sequence
        #each on a new line

    def prefixSuffixGenerator(self, kmers):#dictionary composition = {kmer:(prefix,suffix)}
        '''Iterate through all kmers. Generate prefix and suffix for each Kmer and store in dictionary.
            Return dictionary with suffix and prefix as values for kmer.'''
        prefixSuffixDict = {}
        #set the empty dictionary of prefixes and suffixes correpsonding to each kmer
        for kmer in kmers:
            #iteratre through each kmer in kmers
            prefsuff = []
            #set up an empty list, which will be filled with [prefix,suffix]
            prefsuff.append(kmer[:-1])
            #add the prefix to the list
            prefsuff.append(kmer[1:])
            #add thee suffix to the list
            prefixSuffixDict[kmer] = prefsuff
            #set the kmer as the key and the prefix/suffix list as the value
        return prefixSuffixDict

    def graphGenerator(self, prefixSuffixDict):
        '''Use the prefixSuffixDict to generate an overlap Graph. Iterate through the dictionary containing
            prefixes and suffixes and find overlaps. Generate a dictionary for the overlap graph where
            the Kmer associated with the prefix is a key for the Kmer associated with the overlapping suffix.'''
        graphDict = {}
        #set graphDict equal to a dictionary where the key is a kmer and the value is the next kmer in the sequence
        for kmer1 in prefixSuffixDict:
            #iterate through the prefixSuffixDict and look at one kmer
            prefix = prefixSuffixDict[kmer1][0]
            #the first value in the list value corresponding the kmer key is the prefix
            neighbor = []
            for kmer2 in prefixSuffixDict:
                #iterate through the dictionary within the first loop to find suffixes that are equal to the prefix
                if prefix == prefixSuffixDict[kmer2][1]:
                    #if the prefix and suffix are the same
                    neighbor.append(kmer2)
                    #append the suffix to the list that will be used as the value
                    graphDict[kmer1] = neighbor
                    #set the dictionary to be prefix:suffix
        return(graphDict)

class Usage(Exception):
    '''Signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg


def main(myCommandLine=None):
    '''Run the program.'''
    sequenceFile = sys.stdin
    OverlapGraph(sequenceFile)
if __name__ == "__main__":
    main()