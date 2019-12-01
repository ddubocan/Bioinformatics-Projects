#Program: problem20.py
#Name: Danilo Dubocanin
#Purpose: Given state path and sequence of emissions estimate the parameters for a HMM.


import sys
import math


class ParameterFinder(object):

    def __init__(self, sequenceFile):
        emissions, states, emissionAlphabet, stateAlphabet=self.reader(sequenceFile)
        transitionMatrix, emissionMatrix = self.probs(emissions, states, emissionAlphabet, stateAlphabet)
        print(emissionMatrix, transitionMatrix)


    def reader(self,sequenceFile):
        emissions = sequenceFile.readline().strip()
        sequenceFile.readline()
        emissionAlphabet = sequenceFile.readline().strip().split()
        sequenceFile.readline()
        states = sequenceFile.readline().strip()
        sequenceFile.readline()
        stateAlphabet = sequenceFile.readline().strip().split()
        return(emissions, states, emissionAlphabet, stateAlphabet)

    def probs(self, emissions, states, emissionAlphabet, stateAlphabet):
        emissionMatrix = {}
        transitionMatrix = {}
        for state in stateAlphabet:
            emissionMatrix[state] = {}
            transitionMatrix[state] = {}
            for emission in emissionAlphabet:
                emissionMatrix[state][emission] = 0
            for nextState in stateAlphabet:
                transitionMatrix[state][nextState] = 0
        for pos, state in enumerate(states):
            emissionMatrix[state][emissions[pos]] += 1
            if pos != 0:
                transitionMatrix[states[pos-1]][state] += 1
        for state in stateAlphabet:
            totalTransition = sum(transitionMatrix[state].values())
            totalEmission = sum(emissionMatrix[state].values())

            for count in transitionMatrix[state]:
                transitionMatrix[state][count] = (transitionMatrix[state][count]/totalTransition, 3)

            for count in emissionMatrix[state]:
                emissionMatrix[state][count] = (emissionMatrix[state][count]/totalEmission, 3)



        return(transitionMatrix, emissionMatrix)

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Run the program.'''
    sequenceFile = sys.stdin
    ParameterFinder(sequenceFile)

if __name__ == "__main__":
    main()




###>>> from decimal import localcontext, Decimal, ROUND_HALF_UP
# >>> with localcontext() as ctx:
# ...     ctx.rounding = ROUND_HALF_UP
# ...     for i in range(1, 15, 2):
# ...         n = Decimal(i) / 2
# ...         print(n, '=>', n.to_integral_value())