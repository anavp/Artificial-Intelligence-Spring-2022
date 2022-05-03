import argparse
import os
import csv
import classes

def open_file(filename, mode = 'r'):
    try:
        file = open(filename, mode)
        return file
    except FileNotFoundError:
        print_func(f'The file {filename} was not found. Exiting from the program')
        exit(0)

def static_vars(**kwargs):
    def decorate(func):
        for k, val in kwargs.items():
            setattr(func, k, val)
        return func
    return decorate

@static_vars(outfile = None)
def print_func(message, end = '\n', init = None):
    if print_func.outfile is None and init is not None:
        assert(type(init) == str)
        print_func.outfile = open_file(init, 'w')
    if print_func.outfile is not None:
        print_func.outfile.write(message + end)
    else:
        print(message, end = end)

class writeAction(argparse.Action):
    '''
        This class makes the -w input assume "output.log" as the string input if no file name follows -w in the commandline.   

        For example:

        ```python3 learn -w output2.log [rest of the commands]```
        
        The above command will store "output2.log" in args.w

        ```python3 learn.py -w [rest of the commands]```

        The above command will store "output.log" in args.w. Make sure not to throw the input-file-path positional argument right after -w if you don't want the compiler to assume the output file as the input file given and throw an error that input-file-path positional argument not given.
    '''
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs = nargs, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values) if values is not None else setattr(namespace, self.dest, "output.log")

def parse_args(args = None):
    parser = argparse.ArgumentParser(description = "CSCI-GA.2560 Artificial Intelligence Lab 4 Supervised Machine Learning: kNN and Naive Bayes")
    parser.add_argument('-train', required = True, type = str,\
        help = "pass path of training file")
    parser.add_argument('-test', required = True, type = str,\
        help = "pass path of testing file")
    parser.add_argument('-K', type = int, required = False, default = 0,\
        help = "number of neighbors for kNN")
    parser.add_argument('-C', type = int, required = False, default = 0,\
        help = "laplacian correction constant for Naive Bayes")
    parser.add_argument('-v', required = False, action = 'store_true',\
        help = 'use this tag to enable verbose output')
    parser.add_argument("-w", required = False, type = str, nargs='?', action = writeAction,\
        help = "use this tag to write the output to file called 'output.log' in the same directory")
    parser.add_argument("-debug", required = False, action = 'store_true',\
        help = "use this tag to enable debug mode")
    return parser.parse_args()


def print_args(args):
    print_func(f"-train: {args.train}")
    print_func(f"-test: {args.test}")
    print_func(f"training file: {classes.CONSTANTS.TRAIN}")
    print_func(f"testing file: {classes.CONSTANTS.TEST}")
    print_func(f"-K: {args.K}")
    print_func(f"-C: {args.C}")
    print_func(f"algo: {classes.CONSTANTS.ALGO.name}")
    print_func(f"-w: {args.w}")
    print_func(f"-debug: {args.debug}")

def assert_proper_inputs():
    if classes.CONSTANTS.K > 0 and classes.CONSTANTS.C > 0:
        print_func("K and C both cannot be greater than zero. Exiting...")
        exit(0)
    assert classes.CONSTANTS.ALGO is not None, 'algorithm should have been initialized with either naive bayes or kNN'
    if classes.CONSTANTS.TRAIN is None or os.path.splitext(classes.CONSTANTS.TRAIN)[1] != '.csv':
        print_func("training file must have extension '.csv'. Exiting...")
        exit(0)
    if classes.CONSTANTS.TEST is not None and os.path.splitext(classes.CONSTANTS.TEST)[1] != '.csv':
        print_func("training file must have the extension '.csv'. Exiting...")
        exit(0)

def csv_read(file):
    file = open_file(file)
    file_val = csv.reader(file)
    file_val = list(file_val)
    file.close()
    return file_val

def init(args):
    print_func("", "", args.w)
    classes.CONSTANTS(args.K, args.C, args.train, args.test, args.debug, (classes.ALGORITHM.NAIVE_BAYES if args.K == 0 else classes.ALGORITHM.kNN), args.v)
    # classes.COUNTS()
    assert_proper_inputs()
    if classes.CONSTANTS.DEBUG_MODE:
        print_args(args)
    training_data = csv_read(classes.CONSTANTS.TRAIN)
    testing_data = csv_read(classes.CONSTANTS.TEST)
    return training_data, testing_data


def print_output(counts: classes.COUNTS) -> None:
    # TODO: if classes.CONSTANTS.VERBOSE:
    labels = list(counts.true_positives)
    labels.sort()
    for label in labels:
        precision_denom = counts.true_positives.get(label, 0) + counts.false_positives.get(label, 0)
        recall_denom = counts.true_positives.get(label, 0) + counts.false_negatives.get(label, 0)
        print_func(f"Label={label} Precision={counts.true_positives.get(label, 0)}/{precision_denom} Recall={counts.true_positives.get(label, 0)}/{recall_denom}")
    