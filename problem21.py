#Program: problem21.py
#Name: Danilo Dubocanin
#Purpose: Viterbi Learning


import sys
import problem18
import numpy as np
import operator
import problem20
#iterate between finding a hidden path and then estimating parameter
#use problem18 viterbi algorithm to find hidden path
#use problem 20 parameter estimation to find parameter and then back and forth between these two

#finish print statements
class ViterbiLearning(object):

    def __init__(self, sequenceFile):

        iterationNumber,transitionDict,emissionDict,emissions,pathVariables,sequence = self.reader(sequenceFile)
        for i in range(0, iterationNumber):

            viterbiDict = problem18.HiddenPath.viterbi(self, emissionDict, transitionDict, sequence, pathVariables)
            hiddenPath = problem18.HiddenPath.backTracker(self, viterbiDict, sequence)
            transitionMatrix, emissionMatrix = problem20.ParameterFinder.probs(self, sequence, hiddenPath, emissions, pathVariables)


    def reader(self,sequenceFile):
        iterationNumber = sequenceFile.readline().strip()
        iterationNumber = int(iterationNumber)
        sequenceFile.readline()
        sequence = sequenceFile.readline().strip()
        sequenceFile.readline()
        emissions = sequenceFile.readline().strip().split()
        sequenceFile.readline()
        transitions = sequenceFile.readline().strip().split()
        sequenceFile.readline()
        sequenceFile.readline()
        transitionDict = {}
        # initialize a dictionary that will store the probabilities of transitioning from a state
        # structured as key = state, value = {transition-state: probability}
        for state in transitions:
            # iterate through pathVariables because the next lines have the transition probabilities
            # for each state ordered in the same way as pathVariables
            transitionDict[state] = {}
            # initialize the dictionary that stores all the transition probabilities from a specific state
            trans = sequenceFile.readline().strip().split()
            trans = trans[1:]
            tranProbs = [np.longdouble(prob) for prob in trans]
            # read in all the transition probabilities for a state, remove the first character (equal to state)
            # turn into np.longdouble for increased precision
            for num, transition in enumerate(transitions):
                transitionDict[state][transition] = tranProbs[num]
                # store the transition probabilities for a state with their associated transition state
        sequenceFile.readline()
        sequenceFile.readline()
        # read past a dashed line and then read past a last of headers that is equivalent to emissionVariables
        emissionDict = {}
        # initialize a dictionary that will store the probabilities of emissions from a state
        # structured as key = state, value = {emission: probability}
        for state in transitions:
            # iterate through pathVariables because the next lines have the emission probabilities
            # for each state ordered in the same way as pathVariables
            emissionDict[state] = {}
            # initialize the dictionary that stores all the emission probabilities from a specific state
            emissionProbs = sequenceFile.readline().strip().split()
            emissionProbs = emissionProbs[1:]
            emissionProbs = [np.longdouble(prob) for prob in emissionProbs]
            # read in all the emission probabilities for a state, remove the first character (equal to state)
            # turn into np.longdouble for increased precision
            for num, emitted in enumerate(emissions):
                emissionDict[state][emitted] = emissionProbs[num]
        return(iterationNumber,transitionDict,emissionDict,emissions,transitions,sequence)

    def maxAndPointer(self, state, emissionDict, transitionDict, emission, pos, viterbiDict, pathVariables):
        '''Calculate all possible probabilities for a state to be present at a particular position. Take the highest
            possible probability, assign to the state at that position, and index which previous state it transitioned from.
            Return a list with the probability and the previous state that generated this probability.'''
        emissionProb = emissionDict[state][emission]
        #emissionProb is the probability of emitting that specific emission from that specific state
        possibleProbs = {}
        #initialize the dictionary where key = prior state (hidden), value = probability of the next state given that
        #prior state
        for hidden in pathVariables:
            prob = viterbiDict[pos-1][hidden][0] + np.longdouble(np.log(transitionDict[hidden][state])) + \
                    np.longdouble(np.log(emissionProb))
            possibleProbs[hidden] = prob
        #to find the maximum probability for a state you have to compare all the previous maximum state probabilities, so
        #iterate through all the potential states and calculate the current probability
        top = max(possibleProbs.items(), key=operator.itemgetter(1))[0]
        #adapted this from stackOverflow, finds the maximum probability in the dictionary and outputs the corresponding key
        output = [possibleProbs[top], top]
        #output = [maximum probability at that position, prior state that yields max probability]
        return(output)

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program.'''
    sequenceFile = sys.stdin
    ViterbiLearning(sequenceFile)

if __name__ == "__main__":
    main()


