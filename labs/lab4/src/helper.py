def constants(**kwargs):
    def decorator(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorator

@constants(K = None, C = None, DEBUG_MODE = False)
class CONSTANTS:
    def __init__(self, K, C, debug_mode = False):
        CONSTANTS.K = K
        CONSTANTS.C = C
        CONSTANTS.DEBUG_MODE = debug_mode