from io_helper import *
from gen_helper import *
# TODO: Create readme file; don't forget to explain all -w shit and the way it affects input-file-path positional argument

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

def reset_values(nodes):
    for _, node in nodes.items():
        node.value = 0

def update_policies(nodes):
    policy_updated = False
    for _, node in nodes.items():
        if node.node_type != graph.NODE_TYPE.DECISION_NODE:
            continue
        policy_updated = policy_updated or node.update_policy()
    if policy_updated:
        reset_values(nodes)
    return policy_updated

def value_iteration(nodes):
    one_value_iteration(nodes)
    carry_over_values(nodes)
    nodes[next(iter(nodes))].within_tolerance = False
    iter_count = 0
    while (iter_count < graph.CONSTANTS.iteration_limit and not check_if_within_tolerance(nodes)):
        one_value_iteration(nodes)
        carry_over_values(nodes)
        iter_count += 1
    return update_policies(nodes)

def generic_markov_solver(nodes):
    counter = 0
    while(value_iteration(nodes)):
        counter += 1
        if counter > 1000:
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
