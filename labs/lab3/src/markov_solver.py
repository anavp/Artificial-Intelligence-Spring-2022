from io_helper import *
from gen_helper import *
# TODO: Create readme file; don't forget to explain all -w shit and the way it affects input-file-path positional argument


def generic_markov_solver(tolerance, iteration_limit):
    
    pass

if __name__ == '__main__':
    nodes, args = init()
    if DEBUG_MODE:
        for node_name, node in nodes.items():
            node.print_node()
