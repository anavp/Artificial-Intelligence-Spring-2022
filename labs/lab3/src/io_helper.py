import argparse


def read_input_file(file):
    file = open_file(file)
    lines = file.readlines()
    for line in lines:
        if len(line) == 0:
            continue
        if line[0] == '#':
            continue

class writeAction(argparse.Action):
    '''
        This class makes the -w input assume "../outputs/output.out" as the string input if no file name follows -w in the commandline.   

        For example:

        ```python3 markov_solver -w output2.out [rest of the commands]```
        
        The above command will store "../outputs/output2.out" in args.w

        ```python3 markov_solver.py -w [rest of the commands]```

        The above command will store "../outputs/output.out" in args.w. Make sure not to throw the input-file-path positional argument right after -w if you don't want the compiler to assume the output file as the input file given and throw an error that input-file-path positional argument not given.
    '''
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs = nargs, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None and values[:10] != "../outputs":
            values = "../outputs/" + values
        setattr(namespace, self.dest, values) if values is not None else setattr(namespace, self.dest, "../outputs/output.out")

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

def open_file(filename, mode = 'r'):
    try:
        file = open(filename, mode)
        return file
    except FileNotFoundError:
        print_func(f'The file {filename} was not found. Exiting from the program.')
        exit(0)

@static_vars(outfile = None)
def print_func(message, end = "\n", init = None):
    if print_func.outfile is None and init is not None:
        print_func.outfile = open_file(init, 'w')
    if print_func.outfile is not None:
        print_func.outfile.write(message + end)
    else:
        print(message, end = end)

def read_parse_input_file(file):
    file = open(file, 'r')

def parse_args(args = None):
    parser = argparse.ArgumentParser(description = "CSCI-GA.2560 Artificial Intelligence Lab 3 Generic Markov Solver")
    parser.add_argument("input_file", metavar = "input-file-path", type = str,\
        help = "positional argument that requires the input file path to be given")
    parser.add_argument("-df", type = float, required = False, default = 1.0,\
        help = "-df argument") # TODO: Write proper help statement
    parser.add_argument("-min", required = False, default = False, action = 'store_true',\
        help = "optional argument to minimize values as costs; default value = False") # TODO: Check if this help statement is right
    parser.add_argument("-tol", required = False, type = float, default = 0.01,\
        help = "argument to set float tolerance for exiting value iteration, default value = 0.01") # TODO: Check if this help statement is right
    parser.add_argument("-iter", required = False, type = int, default = 100,\
        help = "argument to set the integer that indicates a cutoff for value iteration, default value = 100") # TODO: Check if this help statement is right
    parser.add_argument("-w", required = False, type = str, nargs='?', action = writeAction,\
        help = "use this tag to write the output to file called 'output.out' in the same directory")
    parser.add_argument("-v", required = False, default = False, action = 'store_true',\
        help = "use this tag to generate the verbose output")
    return parser.parse_args()

def init():
    args = parse_args()
    print_func("", "", args.w)
    return args
