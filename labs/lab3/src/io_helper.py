import argparse
import os
import graph
from gen_helper import *

def process_reward(line, node_dict):
    line = line.replace(' ', '')
    line = line.split('=', -1)
    assert len(line) == 2
    node_name = line[0]
    node_dict = create_node_if_not_exist(node_dict, node_name)
    node_dict[node_name].reward = int(line[-1])
    return node_dict

def process_edges(line, node_dict):
    line = line.replace(" ", "")
    index = line.index(':') # TODO: Use .split instead of .index
    node_name = line[:index]
    # assert node_name in node_dict.keys()
    node_dict = create_node_if_not_exist(node_dict, node_name)
    line = line[index+1:]
    assert ':' not in line
    assert line[0] == '[' and line[-1] == ']'
    line = line[1:-1]
    edges = line.split(',',-1)
    for edge in edges:
        node_dict = create_node_if_not_exist(node_dict, edge)
        node_dict[node_name].add_neighbor(node_dict[edge]) # Assuming uni-directional edges
    return node_dict

def process_probabilities(line, node_dict):
    # line = line.replace(" ", '')
    line = line.split('%', -1)
    assert len(line) == 2
    node_name = line[0].strip()
    assert node_name in node_dict.keys(), "how can the probabilities be assigned if the edges haven't been defined yet!"
    # node_dict = create_node_if_not_exist(node_dict, node_name)
    probabilities = line[1].strip()
    probabilities = probabilities.split()
    cur_node = node_dict[node_name]
    
    for index, prob in enumerate(probabilities):
        probabilities[index] = float(prob)
    
    assert len(probabilities) == len(cur_node.neighbor_list) or len(probabilities) == 1
    if len(probabilities) == 1:
        cur_node.alpha = 1 - probabilities[0]
        cur_node.set_arbitrary_policy()
        cur_node.set_probabilities_by_alpha()
        return node_dict
    sum = 0
    for index, neighbor_name in enumerate(cur_node.neighbor_list):
        neighbor_obj = cur_node.neighbors[neighbor_name]
        neighbor_obj.probability = probabilities[index]
        sum += probabilities[index]
    assert sum == 1, "the sum of given probabilities must be 1"
    return node_dict

def process_input(file):
    file = open_file(file)
    lines = file.readlines()
    node_dict = {}

    for line in lines:
        assert type(line) == str
        if len(line.strip()) == 0:
            print_func("skipping blank line")
            continue
        if line[0] == '#':
            print_func("skipping commented line")
            continue
        assert '#' not in line, "the assumption is that the commented lines have # as their very first character"
        line = line.strip()
        if '=' in line:
            node_dict = process_reward(line, node_dict)
            continue
        elif ':' in line:
            node_dict = process_edges(line, node_dict)
            continue
        elif '%' in line:
            node_dict = process_probabilities(line, node_dict)
    
    return node_dict
        

        

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
        if mode == 'w':
            os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok = True)
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
    node_dict = process_input(args.input_file)
    return node_dict, args
