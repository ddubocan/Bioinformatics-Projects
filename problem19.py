# Name: Danilo Dubocanin
# Program: problem19.py
# Purpose: Given a string of emissions, calculate the total probability that this string of emissions will occur.
#           Implement the Forward Algorithm to find this.


import sys
#import sys to read sys.stdin
import math
#import math to take log probabilities to increase accuracy
from scipy.special import logsumexp
#import logsumexp to add probabilities together in log space
import numpy as np
#import numpy to use longdoubles to increase accuracy
from problem18 import HiddenPath
#problem18 uses the same format of input file, so I import the HiddenPath state to use the reader function

class TotalProb(object):
    '''Calculate the total probability of an emission output given the transition and emission probability matrices.
        To calculate this probability implement the Forward algorithm. Iterate through the emission path and find
        the total probability of each emission occurring at that position. At the end of the path, add together
        probabilities from all states.'''
    def __init__(self, sequenceFile):
        '''Initialize the class. Call reader function from HiddenPath in problem18 to read in file. Call probTracker
            function to generate a dictionary with the total probability for each state at each position. Call the
            probCalc function and use the output of probTracker to generate the total probability of emitting the
            particular emission output.'''
        emissionDict, transitionDict, emissions, pathVariables, emissionVariables = HiddenPath.reader(self, sequenceFile)
        #input sequenceFile and output all the meaningful data within it like the alphabets, probability matrices, and
        #emission. Use the reader from problem18 because they have the same input format
        probDict = self.probTracker(emissionDict, transitionDict, emissions, pathVariables)
        #using the output from the reader calculate the total probability of each state at each position
        prob = self.probCalc(emissions, probDict)
        #input the emissions and the probability dictionary and output the probabilities of the last position all
        #added together
        print(prob)
        #print the probability

    def probTracker(self, emissionDict, transitionDict, emissions, pathVariables):
        '''Implement the Forward Algorithm. Iterate through all the emissions, and at each position add all possible
            probabilities of any of the states occurring at that position. Convert probabilities to log probability
            and use logsumexp to add log probabilities together.'''
        probDict = {}
        #Dictionary is structured as {position:{state: total (sum) of probabilities}}
        for pos, emission in enumerate(emissions):
            probDict[pos] ={}
            #iterate through all the positions in emissions and initialize a dictionary that will store
            #the total probability that a particular state is present at that position
            if pos == 0:
                for state in pathVariables:
                    probDict[pos][state] = math.log(emissionDict[state][emission]) + math.log(1/len(pathVariables))
            #if we are at the begining of the sequence of emissions than the probability that a state is present there
            #is dependent on the start probability (1/len(pathVariables)) and the emission probability from that state
            else:
                for state in pathVariables:
                    probAtPosition = []
                    #iterate through all possible states and initialize a list that will save all the probabilities
                    #leading to each state
                    for priorstate in pathVariables:
                        probAtPosition.append(probDict[pos - 1][priorstate] + math.log(transitionDict[priorstate][state]) +
                                            math.log(emissionDict[state][emission]))
                    #nest a for loop within the initial iteration beause you need to calculate the probability of each
                    #state transition to the current state. add all the probabilities together and append to list
                    probDict[pos][state] = logsumexp(probAtPosition)
                    #logsumexp adds the probabilities together in log space and lets you know the total probability at
                    #that position
        return(probDict)

    def probCalc(self, emissions, probDict):
        '''Calculate the total probability of particular emission using the product of the Forward algorithm.
            Add together the probabilities of all the states in the last position. Convert from log probability
            into normal probability by taking the exponent of the log probability. Return the probability.'''
        states = probDict[len(emissions)-1]
        #all the states and their total probability at the last position in the emission sequence
        theList = []
        for state in states:
            theList.append(states[state])
        #append all the final probabilities of all the states at the last position into a list
        prob = logsumexp(theList)
        #add all the probabilities together
        nonLogProb = math.exp(prob)
        #move from log probability space into probability space
        return(nonLogProb)

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program.'''
    sequenceFile = sys.stdin
    TotalProb(sequenceFile)

if __name__ == "__main__":
    main()