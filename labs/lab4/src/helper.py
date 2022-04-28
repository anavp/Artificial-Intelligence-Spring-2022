from enum import Enum

class ALGORITHM(Enum):
    NAIVE_BAYES = 1
    kNN = 2

def static_constants(**kwargs):
    def decorator(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorator

@static_constants(K = None, C = None, DEBUG_MODE = False, ALGO = None, TRAIN = None, TEST = None, ATTR_CT = -1)
class CONSTANTS:
    def __init__(self, K, C, training_file, testing_file, debug_mode = False, algo = None):
        CONSTANTS.K = K
        CONSTANTS.C = C
        CONSTANTS.DEBUG_MODE = debug_mode
        CONSTANTS.ALGO = algo
        CONSTANTS.TRAIN = training_file
        CONSTANTS.TEST = testing_file
        CONSTANTS.ATTR_CT = -1


class ParserMeta(type):
    """A Parser metaclass that will be used for parser class creation.
    """
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (hasattr(subclass, 'read_input') and
                callable(subclass.read_input) and
                subclass.read_input.__annotations__["return"] == list 
                # and
                # hasattr(subclass, 'value') and
                # callable(subclass.value) and
                # subclass.value.__annotations__["return"] == int and
                # hasattr(subclass, 'restart') and
                # callable(subclass.restart) and
                # subclass.restart.__annotations__["return"] == list and
                # hasattr(subclass, 'tiebreaker') and
                # callable(subclass.tiebreaker) and
                # subclass.tiebreaker.__annotations__["return"] == list
                )

class CLASSIFIER(metaclass = ParserMeta):
    def read_input() -> list:
        pass


# class stateInterface(metaclass = ParserMeta):
#     __writeToFile = None
#     def next(state) -> list:
#         pass
#     def value(state) -> int:
#         pass
#     def goal(self, state) -> bool:
#         return self.value(state) == 0
#     def restart(self) -> list:
#         pass

#     def __init__(self, writeToFile):
#         self.__writeToFile = writeToFile

#     @staticmethod
#     @static_vars(outFile=None)
#     def __write(string,  writeToFile, end = "\n"):
#         if writeToFile and stateInterface.__write.outFile == None:
#             stateInterface.__write.outFile = open("./output.out", 'w')
#         if writeToFile:
#             stateInterface.__write.outFile.write(string + end)
#         else:
#             print(string)
    
#     def printState(self, state = None, prefix = ""):
#         strForPrint = prefix
#         if state is None:
#             self.__write(strForPrint, self.__writeToFile)
#             return
#         listLength = len(state)
#         strForPrint += "["
#         for index, object in enumerate(state):
#             strForPrint += str(object)
#             if index < listLength - 1:
#                 strForPrint += " "
#         strForPrint += "] = " + str(self.value(state))
#         self.__write(strForPrint, self.__writeToFile)

#     def tiebreaker(possibilities) -> list:
#         pass


# class nQueensState(stateInterface):
#     nQueens = -1
#     state = None
#     def __init__(self, n, writeToFile):
#         self.nQueens = n
#         self.state = [i for i in range(self.nQueens)]
#         super().__init__(writeToFile)
    
#     def next(self, state) -> list:
#         neighbors = []
#         for ind1 in range(self.nQueens):
#             for ind2 in range(ind1 + 1, self.nQueens):
#                 state[ind1], state[ind2] = state[ind2], state[ind1]
#                 neighbors.append(copy.deepcopy(state))
#                 state[ind1], state[ind2] = state[ind2], state[ind1]
#         return neighbors
    
#     def value(self, state) -> int:
#         def queensClashing(q1, q2):
#             q1row, q1col = q1
#             q2row, q2col = q2
#             if q1row == q2row or q1col == q2col or q1row + q1col == q2row + q2col or q1row - q1col == q2row - q2col:
#                 return 1
#             return 0
#         error = 0
#         for index, row in enumerate(state):
#             ind2 = index + 1
#             for row2 in state[ind2:]:
#                 error += queensClashing((index, row), (ind2, row2))
#                 ind2 += 1
#         return error
    
#     def restart(self) -> list:
#         random.shuffle(self.state)
#         return self.state
    
#     def tiebreaker(self, possibilities, visitedList = []) -> list:
#         error = self.value(possibilities[0])
#         index = 0
#         while index < len(possibilities):
#             state = possibilities[index]
#             if state in visitedList:
#                 possibilities.remove(state)
#             else:
#                 index += 1
#         return possibilities[random.randint(0, len(possibilities) - 1)]