## Name: Danilo Dubocanin
## Worked With: Kavya Aswadhati, Alex Zee
##Purpose: Given an integer K and a string, find the kmer composition of the string.

import sys  #importing sys so I can read stdin
class AllKmers(object):
    '''Generate the Kmer composition of a string using a text file containing an integer(K) and a DNA string.
        Read in file. Use K to set length of substrings. Iterate through DNA string input and save
        all Kmers of specified size.'''
    def __init__(self, sequenceFile):
        '''Initialize the the class. Use reader function to find K and the DNA string.
            Call kmerMaker function on K and the DNA string to generate a list of Kmers.
            Print Kmers.'''
        k, sequenceString =self.reader(sequenceFile)
        #calling my reader function on the sequencefile to give me the k value and the dna string
        kmers = self.kmerMaker(k, sequenceString)
        #calling my kmer function to turn my dna string into a list of kmers
        kmers.sort()
        #sorting my kmers by alphabetical order
        for kmer in kmers:
            print(kmer)
        #sorting my kmers in alphabetical order and then printing them each on a new line

    def kmerMaker(self, k, sequenceString):
        '''Iterate through DNA string and keep track of position. At each nucleotide position store
            the associated Kmer. Break iteration when newly generated Kmers are shorter than K.
            Store all Kmers and return stored Kmers.'''
        kmers = []
        #set the the kmers list = to an empty list
        for pos, nt in enumerate(sequenceString):
            #using enumerate to go through my string and using the position + the k value
            # to generate my kmers
            kmer = sequenceString[pos:pos+k]
            if len(kmer) != k:
            #if k > number of remaining nucleotides then we need to break out of the for loop
            #because all following kmers will be too small
                break
            kmers.append(kmer)
            #adds kmer to the list of kmers
        return kmers

    def reader(self, sequenceFile):
        '''Read in input File. Read in first line and store as an integer K.
            Read in next line and store as a string. Strip the string of new line
            character. Return K and string containing sequence.'''
        k = int(sequenceFile.readline())
        #the first line of the input file is a number that specifies the kmer length(k)
        sequenceString = sequenceFile.readline()
        #read each line of the input file
        sequenceString = sequenceString.strip()
        #strip of the new line character at the end of each line
        return k, sequenceString

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program. Take in sequenceFile as stdin.
        Call classes necessary to complete task.'''
    sequenceFile = sys.stdin
    AllKmers(sequenceFile)

if __name__ == "__main__":
    main()