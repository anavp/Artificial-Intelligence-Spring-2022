import argparse
import os
import graph

def process_reward(line, nodes):
    line = line.replace(' ', '')
    line = line.split('=', -1)
    assert len(line) == 2
    node_name = line[0]
    nodes = graph.create_node_if_not_exist(nodes, node_name)
    nodes[node_name].reward = int(line[-1])
    return nodes

def process_edges(line, nodes):
    line = line.replace(" ", "")
    line = line.split(':')
    assert len(line) == 2
    node_name = line[0]
    nodes = graph.create_node_if_not_exist(nodes, node_name)
    cur_node = nodes[node_name]
    if cur_node.node_type == graph.NODE_TYPE.TERMINAL_NODE:
        cur_node.node_type = graph.NODE_TYPE.DECISION_NODE
    line = line[1]
    assert ':' not in line
    assert line[0] == '[' and line[-1] == ']'
    line = line[1:-1]
    edges = line.split(',',-1)
    for edge in edges:
        nodes = graph.create_node_if_not_exist(nodes, edge)
        cur_node.add_neighbor(nodes[edge]) # Assuming uni-directional edges
    if cur_node.node_type == graph.NODE_TYPE.DECISION_NODE:
        cur_node.set_arbitrary_policy()
        cur_node.set_probabilities_by_alpha()
    return nodes

def process_probabilities(line, nodes):
    line = line.split('%', -1)
    assert len(line) == 2
    node_name = line[0].strip()
    assert node_name in nodes.keys(), "how can the probabilities be assigned if the edges haven't been defined yet!"
    probabilities = line[1].strip()
    probabilities = probabilities.split()
    cur_node = nodes[node_name]
    
    for index, prob in enumerate(probabilities):
        probabilities[index] = float(prob)
    
    assert len(probabilities) == len(cur_node.neighbor_list) or len(probabilities) == 1

    if len(probabilities) == 1:
        cur_node.alpha = 1 - probabilities[0]
        cur_node.set_arbitrary_policy()
        cur_node.node_type = graph.NODE_TYPE.DECISION_NODE
        cur_node.set_probabilities_by_alpha()
        return nodes

    sum = 0
    for index, neighbor_name in enumerate(cur_node.neighbor_list):
        neighbor_obj = cur_node.neighbors[neighbor_name]
        neighbor_obj.probability = probabilities[index]
        cur_node.node_type = graph.NODE_TYPE.CHANCE_NODE
        sum += probabilities[index]

    assert sum == 1, "the sum of given probabilities must be 1"
    return nodes

def process_input(file):
    file = open_file(file)
    lines = file.readlines()
    nodes = {}

    for line in lines:
        assert type(line) == str
        if len(line.strip()) == 0:
            continue
        if line[0] == '#':
            continue
        assert '#' not in line, "the assumption is that the commented lines have # as their very first character"
        line = line.strip()
        if '=' in line:
            nodes = process_reward(line, nodes)
            continue
        elif ':' in line:
            nodes = process_edges(line, nodes)
            continue
        elif '%' in line:
            nodes = process_probabilities(line, nodes)
    
    return nodes

class writeAction(argparse.Action):
    '''
        This class makes the -w input assume "output.out" as the string input if no file name follows -w in the commandline.   

        For example:

        ```python3 markov_solver -w output2.out [rest of the commands]```
        
        The above command will store "output2.out" in args.w

        ```python3 markov_solver.py -w [rest of the commands]```

        The above command will store "output.out" in args.w. Make sure not to throw the input-file-path positional argument right after -w if you don't want the compiler to assume the output file as the input file given and throw an error that input-file-path positional argument not given.
    '''
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super().__init__(option_strings, dest, nargs = nargs, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values) if values is not None else setattr(namespace, self.dest, "output.out")

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
        help = "float discount factor [0, 1] to use on future rewards, default value = 1.0")
    parser.add_argument("-min", required = False, default = False, action = 'store_true',\
        help = "optional argument to minimize values as costs; default value = False")
    parser.add_argument("-tol", required = False, type = float, default = 0.001,\
        help = "argument to set float tolerance for exiting value iteration, default value = 0.001")
    parser.add_argument("-iter", required = False, type = int, default = 100,\
        help = "argument to set the integer that indicates a cutoff for value iteration, default value = 100")
    parser.add_argument("-w", required = False, type = str, nargs='?', action = writeAction,\
        help = "use this tag to write the output to file called 'output.out' in the same directory")
    return parser.parse_args()

def print_policies(nodes):
    policy_list = list()
    for node_name, node in nodes.items():
        if node.node_type != graph.NODE_TYPE.DECISION_NODE:
            continue
        if len(node.neighbor_list) == 1:
            continue
        policy_list.append(node_name + " -> " + node.policy_name)
    policy_list.sort()
    for policy in policy_list:
        print_func(policy)
    print_func("")

def print_values(nodes):
    value_list = list()
    for node_name, node in nodes.items():
        value_list.append(node_name + '=%.3f'%(node.value))
    value_list.sort()
    for value in value_list:
        print_func(value, end = " ")
    print_func("")

def assert_correct_args(args):
    if args.df > 1 or args.df < 0:
        print ("ERROR: The given discount factor must lie in the interval [0,1]")
        exit(0)
    if args.iter < 0:
        print ("ERROR: The given iteration limit must be positive")
        exit(0)

def init():
    args = parse_args()
    assert_correct_args(args)
    print_func("", "", args.w)
    graph.CONSTANTS(args.df, args.tol, args.iter, args.min)
    nodes = process_input(args.input_file)
    return nodes
