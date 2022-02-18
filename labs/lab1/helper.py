import argparse
import numpy as np

class ParserMeta(type):
    """A Parser metaclass that will be used for parser class creation.
    """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        # TODO: Check if the functions names are correct
        return (hasattr(subclass, 'load_data_source') and 
                callable(subclass.load_data_source) and 
                hasattr(subclass, 'extract_text') and 
                callable(subclass.extract_text))


class stateInterface(metaclass = ParserMeta):
    def actions(state) -> list:
        pass
    def computeError(state) -> int:
        pass

class nQueensState(stateInterface):
    def __init__(self, n = 0):
        numberOfQueens = n
    


def print_args(args):
    print("knapsack-file-path: " + args.knapsackFile)
    print("-N:" + str(args.N))
    print("-verbose: " + str(args.verbose))
    print("-sideways: " + str(args.sideways))
    print("-restarts: " + str(args.restarts))


def intChecker(givenInput):
    num = int(givenInput)
    print(num)
    return num


def parse_args(args = None):
    parser = argparse.ArgumentParser(description="Hill climbing code for AI course")
    parser.add_argument("knapsackFile", metavar = 'knapsack-file-path', type = str, nargs = '?', default="not_defined",\
        help = "pass the path of the knapsack input file")
    parser.add_argument("-N", type = int, required = False, default = -1,\
        help = "the number of queens in the N-Queens problem")
    parser.add_argument("-verbose", required = False, default = False, action = 'store_true',\
        help = "verbose flag somethign something")#TODO: write better description
    # TODO: Improve bad input handling
    parser.add_argument("-sideways", type = intChecker, nargs = '?', required = False, const = 0, default = 0, \
        help = "put the count of sideways steps allowed; default value = 0")
    parser.add_argument("-restarts", type = int, required = False, default = 0, \
        help = "the number of random restarts allowed; default = 0")
    return parser.parse_args()