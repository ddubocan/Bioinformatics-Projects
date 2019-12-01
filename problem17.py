#Program: problem17.py
#Name: Danilo Dubocanin
#Purpose: Computes the probability of an outcome given a hidden path. Takes in as input a text file from Rosalind with a
#state path, emission path, and emission probabilities matrix. Outputs the probability of that emission output given
# the state path .



import sys
#import sys to read stdin
import math
#import math to calculate log probability to increase accuracy
import numpy as np
#use numpy longdouble to increase accuracy

class EmissionProbability(object):
    '''Compute the probability of an emission outcome given a hidden path. Read in an input file with a state path,
        sequence of emissions, and their emission probability matrices. Iterate through the state path and add the log
        probability of the particular emission at that position given that state. Print the probability.'''
    def __init__(self, sequenceFile):
        '''Initialize the class. Read in the file and output the emission matrices, emission sequence and state path.
            Calculate the probability of an outcome of emissions given a hidden path by using the emission matrices,
            emission sequence and state path. Print the probability.'''
        emissionDict, emissions, path = self.reader(sequenceFile)
        prob = self.probOfEmission(emissionDict, emissions, path)
        print(prob)

    def reader(self, sequenceFile):
        '''Read in the file. Save given state and emission paths as strings. Read past dashed lines. Save state alphabet
            as list and iterate through emission matrix using this list. Save probability matrix as dictionaries within a
            dictionary. Import all probabilities as numpy longdoubles. Export state path, emission path, and probability
            matrix.'''
        emissions = sequenceFile.readline().strip()
        #read in a string of sequence of emissions
        sequenceFile.readline()
        #read past dashed line
        emissionVariables = sequenceFile.readline().strip().split()
        #read in a list of the possible different emissions
        sequenceFile.readline()
        #read past dashed line
        path = sequenceFile.readline().strip()
        #read in a string that is markov state path
        sequenceFile.readline()
        #read past dashed line
        pathVariables = sequenceFile.readline().strip().split()
        #read in list of all the possible different states
        sequenceFile.readline()
        sequenceFile.readline()
        #read past a dashed line
        #read past a line consisting of headers, this line is the same as emissionVariables
        emissionDict = {}
        #initialize a dictionary where key = state, value = {emission:probability}
        for state in pathVariables:
            #iterate through all the possible states because we need to have the emission probability associated
            #with each one of them
            emissionDict[state] = {}
            #initialize the dictionary with emission probabilities for each state {emission:probability}
            emissionProbs = sequenceFile.readline().strip().split()
            emissionProbs = emissionProbs[1:]
            emissionProbs = [np.longdouble(prob) for prob in emissionProbs]
            #the number of lines containing emission probabilities is ordered in the same way pathVariables is ordered
            #so each line of emission probabilities corresponds to the state in pathVariables. Read in emission
            #probabilities and convert them all to floats. This is stored in emissionProbs
            for pos, emitted in enumerate(emissionVariables):
                emissionDict[state][emitted] = emissionProbs[pos]
            #iterate through all the emission probabilities stored in emissionVariables and assign the emission and its
            #probability to the current, corresponding state
        return(emissionDict, emissions, path)

    def probOfEmission(self, emissionDict, emissions, path):
        '''Calculate the probability of the emission with the given path. Initialize log probability. Iterate through
            state path and add the log probability of emitting the particular emission at that particular state. Take
            the exponent of the log probability. Return probability.'''
        prob = math.log(1)
        #intialize the probability(=1) and take the log (for accuracy)
        for pos, state in enumerate(path):
            prob += math.log(emissionDict[state][emissions[pos]])
        #Iterate through the state path(path) and keep track of position so you can index the corresponding emission
        #in emissions. When you know the state, and emission you can take the probability our of the emission Dictionary
        #and add it to the log probability.
        nonLogProb = math.exp(prob)
        #convert from log probability to probability
        return(nonLogProb)

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program.'''
    sequenceFile = sys.stdin
    EmissionProbability(sequenceFile)

if __name__ == "__main__":
    main()