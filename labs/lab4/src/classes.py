from enum import Enum
import io_helper

class ALGORITHM(Enum):
    NAIVE_BAYES = 1
    kNN = 2

def static_constants(**kwargs):
    def decorator(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorator

@static_constants(K = None, C = None, DEBUG_MODE = False, ALGO = None, TRAIN = None, TEST = None, ATTR_CT = -1, VERBOSE = None)
class CONSTANTS:
    def __init__(self, K, C, training_file, testing_file, debug_mode = False, algo = None, verbose = False):
        CONSTANTS.K = K
        CONSTANTS.C = C
        CONSTANTS.DEBUG_MODE = debug_mode
        CONSTANTS.ALGO = algo
        CONSTANTS.TRAIN = training_file
        CONSTANTS.TEST = testing_file
        CONSTANTS.ATTR_CT = -1
        CONSTANTS.VERBOSE = verbose

# @static_values(true_positives = 0, false_positives = 0, true_negatives = 0, false_negatives = 0)
class COUNTS:
    true_positives = dict()
    false_positives = dict()
    true_negatives = dict()
    false_negatives = dict()
    
    def __init__(self):
        self.true_positives = dict()
        self.false_positives = dict()
        self.true_negatives = dict()
        self.false_negatives = dict()


class ClassifierMeta(type):
    def __instancecheck__(cls, __instance) -> bool:
        return cls.__subclasscheck__(type(__instance))

    def __subclasscheck__(cls, __subclass: type) -> bool:
        return (
            hasattr(__subclass, 'train') and
            callable(__subclass.train) and
            __subclass.train.__annotations__["return"] == list and
            hasattr(__subclass, 'test') and
            callable(__subclass.test) and
            __subclass.test.__annotations__["return"] == COUNTS
        )

class CLASSIFIER(metaclass = ClassifierMeta):
    def train() -> list:
        pass

    def test() -> COUNTS:
        pass

class RECORD:
    attributes = list()
    attribute_ct = -1
    label = None

    def __init__(self, *args):
        self.attribute_ct = len(args) - 1
        # io_helper.print_func(f"debug: {args}")
        for attr in args[:-1]:
            self.attributes.append(attr)
        self.label = args[-1]

class DataMeta(type):
    def __instancecheck__(cls, __instance) -> bool:
        return cls.__subclasscheck__(type(__instance))
    
    def __subclasscheck__(cls, __subclass: type) -> bool:
        return (
            hasattr(__subclass, 'add_record') and
            callable(__subclass.add_record) and
            __subclass.add_record.__annotations__["return"] == None
        )

class DATA:
    records = list()
    attribute_ct = -1
    record_count = 0

    def __init__(self):
        self.records = list()
        self.attribute_ct = -1
        self.record_count = 0

    def add_record(self, values) -> None:
        pass