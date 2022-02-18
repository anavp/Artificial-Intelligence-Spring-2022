import argparse
import json
import copy

class ParserMeta(type):
    """A Parser metaclass that will be used for parser class creation.
    """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        # TODO: Check if the functions names are correct
        return (hasattr(subclass, 'Next') and
                callable(subclass.Next) and
                subclass.Next.__annotations__["return"] == list and
                hasattr(subclass, 'Value') and
                callable(subclass.Value) and
                subclass.Value.__annotations__["return"] == int)# and


class stateInterface(metaclass = ParserMeta):
    def Next(state) -> list:
        pass
    def Value(state) -> int:
        pass
    def goal(self, state) -> bool:
        return self.Value(state) == 0


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


class nQueensState(stateInterface):
    nQueens = -1
    state = None
    def __init__(self, n):
        self.nQueens = n
        self.state = [i for i in range(self.nQueens)]
    
    def Next(self, state) -> list:
        neighbors = []
        for ind1 in range(self.nQueens):
            for ind2 in range(ind1 + 1, self.nQueens):
                state[ind1], state[ind2] = state[ind2], state[ind1]
                neighbors.append(copy.deepcopy(state))
                state[ind1], state[ind2] = state[ind2], state[ind1]
        return neighbors
    
    def Value(self, state) -> int:
        def queensClashing(q1, q2):
            q1row, q1col = q1
            q2row, q2col = q2
            if q1row == q2row or q1col == q2col or q1row + q1col == q2row + q2col or q1row - q1col == q2row - q2col:
                return 1
            return 0
        error = 0
        for index, row in enumerate(state):
            ind2 = index + 1
            for row2 in state[ind2:]:
                error += queensClashing((index, row), (ind2, row2))
                ind2 += 1
        return error
    
    def printThings(self):
        print("numberOfQueens: " + str(self.nQueens))
        print("state: " + str(self.state))


class knapsackState(stateInterface):
    state = None
    T, M = -1, -1
    objects = {}
    allObjects = []
    def __init__(self, jsonFile):
        jsonFile = open(jsonFile)
        data = json.load(jsonFile)
        self.T, self.M = data['T'], data['M']
        for item in data['Items']:
            self.objects[item['name']] = item
            self.allObjects.append(item['name'])
        self.state = data['Start']

    def Next(self, state) -> list:
        diff = list(set(self.allObjects) - set(state))
        diff.sort()
        neighbors = []
        
        # Add an object
        for object in diff:
            neighbor = state + [object]
            neighbor.sort()
            neighbors.append(neighbor)
        
        # Remove an object
        for object in state:
            neighbor = list(set(state) - set(object))
            neighbor.sort()
            neighbors.append(neighbor)

        # Swap an object
        for object in diff:
            for element in state:
                neighbor = list(set.union(set(state) - set(element), set(object)))
                neighbor.sort()
                neighbors.append(neighbor)
        
        return neighbors
    
    def Value(self, state) -> int:
        totalWeight, totalValue = 0, 0
        for object in state:
            totalWeight += self.objects[object]['W']
            totalValue += self.objects[object]['V']
        return max(totalWeight - self.M, 0) + max(self.T - totalValue, 0)

    def printThings(self):
        print(self.state)
        for item, value in self.objects.items():
            print(item + ": " + str(value))


def getObject(args):
    if args.N == -1:
        return knapsackState(args.knapsackFile)
    else:
        return nQueensState(args.N)


def print_args(args):
    print("knapsack-file-path: " + args.knapsackFile)
    print("-N:" + str(args.N))
    print("-verbose: " + str(args.verbose))
    print("-sideways: " + str(args.sideways))
    print("-restarts: " + str(args.restarts))


def intChecker(givenInput):
    num = int(givenInput)
    return num


def verifyIfGoodArgumentsGiven(args):
    if args.knapsackFile == "not_defined" and args.N == -1:
        print("ERROR: Either number of queens should be defined or a knapsack file must be passed")
        print("     Have a look at the positional and optional arguments by running 'python hillClimb.py --help'")
        exit(0)


def assertThatTheClassIsGood():
    assert issubclass(nQueensState, stateInterface), "nQueensState is not a subclass of stateInterface"
    assert issubclass(knapsackState, stateInterface), "knapsackState is not a subclass of stateInterface"


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


def writeState(state, error):
    listLength = len(state)
    write("[", end = "")
    for index, object in enumerate(state):
        if index < listLength - 1:
            write(object, end = " ")
        else:
            write(str(object) + "] = " + str(error))


def printState(state, error):
    listLength = len(state)
    print("[", end = "")
    for index, object in enumerate(state):
        if index < listLength - 1:
            print(object, end = " ")
        else:
            print(object + "] = " + str(error))


@static_vars(outFile=None)
def write(string, end = "\n", fileName = "./output.out"):
    if write.outFile == None:
        write.outFile = open(fileName, 'w')
    string = str(string)
    write.outFile.write(string + end)
