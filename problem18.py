# Name: Danilo Dubocanin
# Program: problem18.py
# Purpose: Implement the Viterbi Algorithm. Given a string of emissions, emission probabilities, and transition
#          probabilities, calculate the most probable state path.


import sys
#import sys to read sys.stdin
import math
#import math for log probabilities
import operator
#import operator to find the max value in a dictionary
import numpy as np
#import numpy to use longdoubles for increased accuracy

class HiddenPath(object):
    '''Generate the most probable state path given a string of emissions. Read in a file with a string of emissions,
        emission and state alphabets, and emission and transition probability matrices. Using the input data, implement
        the Viterbi algorithm. Traverse the emission string, calculating the maximum probability for each state at
        each position. Backtrack through the Viterbi graph from the most probable end state.'''
    def __init__(self, sequenceFile):
        '''Initialize the class. Read in the file and return the probability matrices, the transition and emission
            alphabets, and the emission string. Using the output from the reader function, generate a graph using the
            Viterbi algorithm. Using this Viterbi graph, backtrack through the graph and output the state path.
            Print the state path.'''
        emissionDict, transitionDict, emissions, pathVariables, emissionVariables = self.reader(sequenceFile)
        viterbiDict = self.viterbi(emissionDict, transitionDict, emissions, pathVariables)
        statePath = self.backTracker(viterbiDict, emissions)
        return(statePath)
        print(statePath)


    def reader(self, sequenceFile):
        '''Read in the file. Save given emission paths as a string. Read past dashed lines. Save state and emission
            alphabet as lists and iterate through transition and emission matrices using these lists, respectively.
            Save probability matrices as dictionaries within a dictionaries. Import all probabilities as numpy longdoubles.
            Return transition and emission matrices, emission string, and lists with the emission and state alphabet.'''
        emissions = sequenceFile.readline().strip()
        #read in string of emissions
        sequenceFile.readline()
        #read past dashed line
        emissionVariables = sequenceFile.readline().strip().split()
        #read in the alphabet that makes up all the possible emissions as a list
        sequenceFile.readline()
        #read past a dashed line
        pathVariables = sequenceFile.readline().strip().split()
        #read in the alphabet that makes up all the possible states as a list
        sequenceFile.readline()
        sequenceFile.readline()
        #read past a dashed line and then read past a list of headers that is equivalent to pathVariables
        transitionDict = {}
        #initialize a dictionary that will store the probabilities of transitioning from a state
        #structured as key = state, value = {transition-state: probability}
        for state in pathVariables:
            #iterate through pathVariables because the next lines have the transition probabilities
            #for each state ordered in the same way as pathVariables
            transitionDict[state] = {}
            #initialize the dictionary that stores all the transition probabilities from a specific state
            trans = sequenceFile.readline().strip().split()
            trans = trans[1:]
            tranProbs = [np.longdouble(prob) for prob in trans]
            #read in all the transition probabilities for a state, remove the first character (equal to state)
            #turn into np.longdouble for increased precision
            for num, transition in enumerate(pathVariables):
                transitionDict[state][transition] = tranProbs[num]
                #store the transition probabilities for a state with their associated transition state
        sequenceFile.readline()
        sequenceFile.readline()
        #read past a dashed line and then read past a last of headers that is equivalent to emissionVariables
        emissionDict = {}
        #initialize a dictionary that will store the probabilities of emissions from a state
        #structured as key = state, value = {emission: probability}
        for state in pathVariables:
            # iterate through pathVariables because the next lines have the emission probabilities
            # for each state ordered in the same way as pathVariables
            emissionDict[state] = {}
            # initialize the dictionary that stores all the emission probabilities from a specific state
            emissionProbs = sequenceFile.readline().strip().split()
            emissionProbs = emissionProbs[1:]
            emissionProbs = [np.longdouble(prob) for prob in emissionProbs]
            # read in all the emission probabilities for a state, remove the first character (equal to state)
            # turn into np.longdouble for increased precision
            for num, emitted in enumerate(emissionVariables):
                emissionDict[state][emitted] = emissionProbs[num]
            # store the emission probabilities for a state with their associated emission for each state
        return(emissionDict, transitionDict, emissions, pathVariables, emissionVariables)

    def viterbi(self, emissionDict, transitionDict, emissions, pathVariables):
        '''Implement Viterbi Algorithm. Initialize a dictionary. Iterate through each position of the emission string
            and add an entry corresponding to each position. For each position, keep track of the highest probability for
            each state to occur there, and index which state it transitioned from to get the highest probability. Use
            maxAndPointer helper function to find the maximum probability at each position. When the entire emission output
            has been traversed return the Viterbi graph, in the form of its dictionary.'''
        viterbiDict ={}
        #intitialize dictionary where key = position in emissions(pos), value = {state:[maximum probability,
        # prior-state}
        for pos, emission in enumerate(emissions):
            #iterate through the sequence of emissions because we need to find the highest probability for a state
            #at each position, keep track of the position we are at because that is the key in our dictionary
            #and lets us access the previous emission/states/probabilities
            viterbiDict[pos]= {}
            #initialize the dictionary storing the highest probability for each state at each position
            if pos == 0:
                for state in pathVariables:
                    viterbiDict[pos][state] = [np.longdouble(np.log(emissionDict[state][emission])), 'start']
                #if we are the 0th position of emissions, then our probability is only dependent on the emission
                #probability at that state, and the state we came from is 'start'
            else:
                for state in pathVariables:
                    viterbiDict[pos][state] = self.maxAndPointer(state, emissionDict, transitionDict, emission, pos,
                                                                 viterbiDict,pathVariables)
                #the maximum probability for each state at each position is dependent on the maximum probability
                #between the two states in the prior position, maxAndPointer is a helper function that will let us
                #find the maximum probability for each state at a position, and index the state it transitioned from
        return(viterbiDict)

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

    def backTracker(self, viterbiDict, emissions):
        '''Generate the most probable state path by backtracking through the Viterbi Graph. Create a list and insert the
            state with the highest probability corresponding to the last emission. Iterate through the positions of the
            emission sequence backwards, use the positions to access state probabilities. Use the most recent addition
            to the state list to access which state it transitioned from. Insert this state at the 0th position of the
            state list. Join the list and return the corresponding string of states.'''
        stateSeq = []
        stateSeq.append(max(viterbiDict[len(emissions)-1].items(), key=operator.itemgetter(1))[0][0])
        #use operator.itemgetter to find the final key (final state) with the highest value (most probable)
        for pos in range(len(emissions)-1,0,-1):
            stateSeq.insert(0, viterbiDict[pos][stateSeq[0]][1])
        #traverse the most probable path of states, by starting at at the last position in the state path.
        #each position value in the dictionary points back to the path ir originated from. if you just insert
        #these at the beginning of a list and join the list together you get the state path
        stateSeq = ''.join(stateSeq)
        #join list together
        return(stateSeq)

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program.'''
    sequenceFile = sys.stdin
    HiddenPath(sequenceFile)

if __name__ == "__main__":
    main()