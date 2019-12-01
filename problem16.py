#Program: problem16.py
#Name: Danilo Dubocanin
#Purpose: Computes the probability of a hidden path. Takes in as input an text file from Rosalind with a
#state path, and transition probabilities matrix. Outputs the probability of that state path.


import sys
#import sys to use sys.stdin
import math
#import math to use log probabilities to increase accuracy
import numpy as np
#import numpy to use numpy floats (longdouble) to increase accuracy

class HiddenPathProbability(object):
    '''Calculate the probability of a hidden Markov State Path. Read in a text file with a state path, alphabet of states,
        and transition matrices. Use the transition probabilities to calculate the probability of the given state path
        Print out the total calculated probability..'''
    def __init__(self, sequenceFile):
        '''Initialize the class. Read in the input file using reader function. Reader function will output the state
            path, transition probability matrices, and the number of different states. Use these to calculate the
            path probability using the probability function.'''
        statePath, transitionDict, numOfStates = self.reader(sequenceFile)
        #This function will read in the input file (Rosalind formatted) and return the state path as a string,
        # the transition probabilities as a dictionary of dictionaries, and the number of possible states
        prob = self.probability(statePath, transitionDict,numOfStates)
        #This function will use the state path, transition probabilities, and number of possible states
        #to calculate the probability and return the probability
        print(prob)

    def reader(self, sequenceFile):
        '''Read in the file. Save given state path as string. Read past dashed lines. Save state alphabet as list and
            iteratethrough transition matrix using this list. Save the number of different states. Save probability
            matrix as dictionaries within a dictionary. Import all probabilities as numpy longdoubles. Export state path,
            transition matrix,and number of different states.'''
        statePath = sequenceFile.readline().strip()
        #read in the path of the Markov States, strip of new line character at the end
        sequenceFile.readline()
        #reads past dashed line
        pathVariables = sequenceFile.readline().strip().split()
        #reads in the alphabet that makes up the possible states, strip new line character, and splits
        #the string into a list
        numOfStates = len(pathVariables)
        #The number of different states will be used to calculate the starting probability for any state.
        sequenceFile.readline()
        #read past another dashed line
        transitionDict = {}
        #initialize an empty dictionary where the key = state, value = {next state: transition probability}
        sequenceFile.readline()
        #read past the column headers for the transition probabilities, these are ordered the same way as the
        #pathVariables list, so we can use that to assign transition probabilities to the appropriate state variable
        for state in pathVariables:
            transitionDict[state] = {}
            #iterate through all potential state variables and populate the dictionary
            trans = sequenceFile.readline().strip().split()
            trans = trans[1:]
            tranProbs = [np.longdouble(prob) for prob in trans]
            #For every state in pathVariables, there will be a line with its transition probabilities. Read in the line,
            #remove new line character, and turn it into a list (trans), remove first character (it is equal to state).
            #Use list comprehension to make all transition probabilities numpy longdouble floats to increase precision
            for num, transition in enumerate(pathVariables):
                transitionDict[state][transition] = tranProbs[num]
            #for every state, there will be transitions to every other state. Nest a forloop where we iterate
            #through all the potential transitions for a state. The transition probability position
            #in tranProbs is equal to the the position of that state in pathvariables so we can use enumerate to
            #to be able to efficiently index position of the probability while also keeping track of which state
            #we are transitioning to
        return(statePath, transitionDict,numOfStates)

    def probability(self, statePath, transitionDict, numOfStates):
        '''Calculate probability. Calculate probability in log space to increase accuracy. Find starting probability by
            dividing 1 by the number of states. Iterate through the path of states, and add  the log probability of
            transitioning to that particular state to the total log probability. Return the exponent of the log
            probability.'''
        prob = np.longdouble(math.log(1.0/numOfStates))
        #we are assuming equal probability between starting at any of the states, so the starting
        # probability for any particular state is just 1/numOfStates(# of possible states)
        #take the log probability to increase accuracy
        for pos, state in enumerate(statePath):
            #we need to iterate through the entire path of states and both keep track of the
            #current state we are at, and the state that occurred prior. To do that we will keep
            #track of our position so we can reference the prior state variable (statePath[pos-1])
            #and know the current state (state). By using enumerate, we can do that
            if pos == 0:
                continue
            #if pos == 0: then we are the start of the path. We already accounted for start transition.
            else:
                prob += math.log(transitionDict[statePath[pos-1]][state])
            #if pos != 0, we add the log probability of the transition from the prior state (statePath[pos-1]),
            #to the current state (state). Use log probabilities instead of normal probabilities to increase accuracy.
            #Adding log probabilities is equivalent to multiplying probabilities. The probablitiy of a state path
            #is a conditional probability, so we would multiply transition probabilities together, and in terms of log
            #probabilities, we would add them together
        nonLogProb =math.exp(prob)
        #To convert a log probability into normal probability we just need to take its exponenet (e^prob)
        return(nonLogProb)

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program.'''
    sequenceFile = sys.stdin
    HiddenPathProbability(sequenceFile)

if __name__ == "__main__":
    main()