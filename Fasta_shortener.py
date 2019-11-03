

from fastaReader import FastAreader #Need to import this to read the genomic sequence out of the Fasta file. From Prof. Bernick
import argparse


class Shortener(object):
    def __init__(self, mySequences, start, end):
        output = self.seqShortener(mySequences, start, end)
        for head, sequence in output:
            print('>'+head)
            print(sequence)

    def seqShortener(self, mySequences, start, end):
        size = end - start
        outputList = []
        start = int(start)
        end = int(end)
        for head, sequence in mySequences:
            if len(sequence) < start:
                continue
            elif len(sequence) < size:
                continue
            else:
                outputSeq = sequence[start:end+1]
            outputList.append((head, outputSeq))
        return outputList


def userInput():
    '''Handle the user input from Command line to set the min and max size of the K-mer and the Z-cutoff.'''
    parser = argparse.ArgumentParser()#Kavya Aswadhati helped me with this, adapted from what Prof. Bernick gave us
    parser.add_argument("-start", "--seqStart" , type = float, help = "input filename")
    parser.add_argument("-end", "--seqEnd", type = int, help = "input filename")
    args = parser.parse_args()
    return args.seqStart, args.seqEnd

class Usage(Exception):
    '''Used to signal a Usage error, evoking a usage statement and eventual exit when raised.'''
    def __init__(self, msg):
        self.msg = msg

def main(myCommandLine=None):
    '''Implement the Usage exception handler that can be raised from anywhere in process.'''
    mySequences = []       #generate an empty list to be populated with strings of genomic sequence
    theReader = FastAreader()   #utilize the fasta reader that Prof. Bernick developed
    for head, sequence in theReader.readFasta():
        mySequences.append((head,sequence))
    start, end = userInput()
    Shortener(mySequences, start, end )

if __name__ == "__main__":
    main()