from curses.ascii import isdigit
import json
import copy
import random
import argparse

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


class ParserMeta(type):
    """A Parser metaclass that will be used for parser class creation.
    """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        # TODO: Check if the functions names are correct
        return (hasattr(subclass, 'next') and
                callable(subclass.next) and
                subclass.next.__annotations__["return"] == list and
                hasattr(subclass, 'value') and
                callable(subclass.value) and
                subclass.value.__annotations__["return"] == int and
                hasattr(subclass, 'restart') and
                callable(subclass.restart) and
                subclass.restart.__annotations__["return"] == list and
                hasattr(subclass, 'tiebreaker') and
                callable(subclass.tiebreaker) and
                subclass.tiebreaker.__annotations__["return"] == list
        )


class stateInterface(metaclass = ParserMeta):
    __writeToFile = None
    def next(state) -> list:
        pass
    def value(state) -> int:
        pass
    def goal(self, state) -> bool:
        return self.value(state) == 0
    def restart(self) -> list:
        pass

    def __init__(self, writeToFile):
        self.__writeToFile = writeToFile

    @staticmethod
    @static_vars(outFile=None)
    def __write(string,  writeToFile, end = "\n"):
        if writeToFile and stateInterface.__write.outFile == None:
            stateInterface.__write.outFile = open("./output.out", 'w')
        if writeToFile:
            stateInterface.__write.outFile.write(string + end)
        else:
            print(string)
    
    def printState(self, state = None, prefix = ""):
        strForPrint = prefix
        if state is None:
            self.__write(strForPrint, self.__writeToFile)
            return
        listLength = len(state)
        strForPrint += "["
        # for index, object in enumerate(state):
        for index, object in enumerate(state):
            # strForPrint += str(object) + " "
            if index < listLength - 1:
                strForPrint += str(object) + " "
            else:
                strForPrint += str(object)
        strForPrint += "] = " + str(self.value(state))
        self.__write(strForPrint, self.__writeToFile)

    def tiebreaker(possibilities) -> list:
        pass


class nQueensState(stateInterface):
    nQueens = -1
    state = None
    def __init__(self, n, writeToFile):
        self.nQueens = n
        self.state = [i for i in range(self.nQueens)]
        super().__init__(writeToFile)
    
    def next(self, state) -> list:
        neighbors = []
        for ind1 in range(self.nQueens):
            for ind2 in range(ind1 + 1, self.nQueens):
                state[ind1], state[ind2] = state[ind2], state[ind1]
                neighbors.append(copy.deepcopy(state))
                state[ind1], state[ind2] = state[ind2], state[ind1]
        return neighbors
    
    def value(self, state) -> int:
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
    
    def restart(self) -> list:
        random.shuffle(self.state)
        return self.state
    
    def tiebreaker(self, possibilities, visitedList = []) -> list:
        assert len(visitedList) != 0 or len(possibilities) > 1, "tiebreaker should only kick in when it's needed"
        error = self.value(possibilities[0])
        index = 0
        while index < len(possibilities):
            state = possibilities[index]
            assert self.value(state) == error, "all states in possibilities should have the same error"
            if state in visitedList:
                possibilities.remove(state)
            else:
                index += 1
        return possibilities[random.randint(0, len(possibilities) - 1)]
    
    def printThings(self):
        print("numberOfQueens: " + str(self.nQueens))
        print("state: " + str(self.state))


class knapsackState(stateInterface):
    state = None
    T, M = -1, -1
    __objects = {}
    allObjects = []
    def __init__(self, jsonFile, writeToFile):
        class objectClass:
            name = None
            value = None
            weight = None
            def __init__(self, name, value, weight):
                self.name = name
                self.value = int(value)
                self.weight = int(weight)
            def __str__(self):
                return f'{self.name} = [{self.value}, {self.weight}]'
        super().__init__(writeToFile)
        jsonFile = open(jsonFile)
        data = json.load(jsonFile)
        self.T, self.M = data['T'], data['M']
        for item in data['Items']:
            self.__objects[item['name']] = objectClass(name = item['name'], value = item['V'], weight = item['W'])
            self.allObjects.append(item['name'])
        self.state = data['Start']

    def next(self, state) -> list:
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

    def __getTotalValueAndWeight(self, givenState):
        totalValue, totalWeight = 0, 0
        for item in givenState:
            totalValue += self.__objects[item].value
            totalWeight += self.__objects[item].weight
        return totalValue, totalWeight

    def value(self, givenState) -> int:
        totalValue, totalWeight = self.__getTotalValueAndWeight(givenState)
        return max(totalWeight - self.M, 0) + max(self.T - totalValue, 0)

    def restart(self) -> list:
        self.state = random.sample(self.allObjects, random.randint(1, len(self.allObjects)))
        self.state.sort()
        return self.state

    def tiebreaker(self, possibilities, visitedList = []) -> list:
        assert len(visitedList) != 0 or len(possibilities) > 1, "tiebreaker should only kick in when it's needed"
        error = self.value(possibilities[0])
        selectedState = possibilities[0]
        value, weight = self.__getTotalValueAndWeight(selectedState)
        index = 1
        while index < len(possibilities):
            state = possibilities[index]
            assert self.value(state) == error, "all states in possibilities should have the same error"
            if state in visitedList:
                possibilities.remove(state)
                continue
            curValue, curWeight = self.__getTotalValueAndWeight(state)
            if curValue > value or (curValue == value and curWeight < weight):
                selectedState = state
            index += 1
        if selectedState in visitedList:
            return None
        else:
            return selectedState
    
    def printThings(self):
        print(self.state)
        print("T: " + str(self.T))
        print("M: " + str(self.M))
        for item, value in self.__objects.items():
            print(str(value))


def getObject(args):
    if args.N == -1:
        return knapsackState(args.knapsackFile, args.w)
    else:
        return nQueensState(args.N, args.w)


def print_args(args):
    print("knapsack-file-path: " + args.knapsackFile)
    print("-N:" + str(args.N))
    print("-verbose: " + str(args.verbose))
    print("-sideways: " + str(args.sideways))
    print("-restarts: " + str(args.restarts))


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
    parser.add_argument("-sideways", type = int, nargs = '?', required = False, const = 0, default = 0, \
        help = "put the count of sideways steps allowed; default value = 0")
    parser.add_argument("-restarts", type = int, required = False, default = 0, \
        help = "the number of random restarts allowed; default = 0")
    parser.add_argument("-w", required = False, default = False, action = 'store_true',\
        help = "use this tag to write the output to file called 'output.out' in the same directory")
    return parser.parse_args()