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
        return (
                hasattr(subclass, 'train') and
                callable(subclass.train) and
                subclass.train.__annotations__["return"] == list
                )

class CLASSIFIER(metaclass = ParserMeta):
    def train() -> list:
        pass

class RECORD:
    attributes = list()
    attribute_ct = -1
    label = None

    def __init__(self, *args):
        self.attribute_ct = len(args) - 1
        for attr in args[:-1]:
            self.attributes.append(attr)
        self.label = args[-1]


class DATA:
    records = list()
    label_counts = dict()
    attr_counts = list()
    __record_count = 0
    __attr_count = -1

    def __init__(self):
        self.records = list()
        self.label_count = dict()
        self.__record_count = 0
        self.attr_counts = list()
        self.__attr_count = -1
    
    def __init_attr_counts(self):
        assert self.__attr_count != -1
        for _ in range(self.__attr_count):
            self.attr_counts.append(dict())
    
    def __update_attr_counts(self, label, *args):
        assert len(self.attr_counts) == self.__attr_count
        for i in range(self.__attr_count):
            self.attr_counts[i][label] = self.attr_counts[i].get(label, 0) + 1

    def add_record(self, values):
        self.records.append(RECORD(*values))
        if self.__attr_count == -1:
            self.__attr_count = self.records[-1].attribute_ct
            self.__init_attr_counts()
        label = self.records[-1].label
        self.label_counts[label] = self.label_counts.get(label, 0) + 1
        self.__record_count += 1
        self.__update_attr_counts(label, *self.records[-1].attributes)
        assert self.__record_count == len(self.records)