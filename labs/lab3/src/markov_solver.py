from io_helper import *
import gen_helper
# TODO: Create readme file; don't forget to explain all -w shit and the way it affects input-file-path positional argument

def set_chance_nodes_probabilities(nodes):
    for _, node in nodes.items():
        if node.node_type != graph.NODE_TYPE.CHANCE_NODE:
            continue
        node.set_chance_node_probabilities()

def check_if_within_tolerance(nodes):
    for _, cur_node in nodes.items():
        if not cur_node.within_tolerance:
            return False
    return True

def carry_over_values(nodes):
    for _, node in nodes.items():
        node.carry_over_value()

def one_value_iteration(nodes):
    for _, node in nodes.items():
        node.update_value()

def set_terminal_nodes(nodes):
    for _, node in nodes.items():
        if node.node_type != graph.NODE_TYPE.TERMINAL_NODE:
            continue
        node.update_value()

def reset_values(nodes):
    for _, node in nodes.items():
        if node.node_type == graph.NODE_TYPE.TERMINAL_NODE:
            continue
        node.value = 0

def update_policies(nodes):
    policy_updated = False
    for _, node in nodes.items():
        if node.node_type != graph.NODE_TYPE.DECISION_NODE:
            continue
        policy_updated = node.update_policy() or policy_updated
    if policy_updated:
        if gen_helper.DEBUG_MODE:
            print_nodes(nodes)
        reset_values(nodes)
    return policy_updated

def value_iteration(nodes):
    set_terminal_nodes(nodes)
    carry_over_values(nodes)
    if gen_helper.DEBUG_MODE:
        print_nodes(nodes)
    nodes[next(iter(nodes))].within_tolerance = False
    iter_count = 0
    while (iter_count < graph.CONSTANTS.iteration_limit and not check_if_within_tolerance(nodes)):
        one_value_iteration(nodes)
        carry_over_values(nodes)
        iter_count += 1
    return update_policies(nodes)

def generic_markov_solver(nodes):
    counter = 0
    set_chance_nodes_probabilities(nodes)
    
    while(value_iteration(nodes)):
        counter += 1
        if counter > 100:
            print_func("counter break!!!!!")
            break
    
def print_policies(nodes):
    policy_list = list()
    for node_name, node in nodes.items():
        if node.node_type != graph.NODE_TYPE.DECISION_NODE:
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

if __name__ == '__main__':
    nodes, args = init()
    generic_markov_solver(nodes)
    print_policies(nodes)
    print_values(nodes)
