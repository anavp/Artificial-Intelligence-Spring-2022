from io_helper import *
# TODO: Create readme file; don't forget to explain all -w shit and the way it affects input-file-path positional argument

def set_chance_nodes_probabilities(nodes):
    for _, node in nodes.items():
        if node.node_type == graph.NODE_TYPE.CHANCE_NODE:
            node.set_chance_node_probabilities()

def assert_proper_input(nodes):
    for _,node in nodes.items():
        node.assert_proper_input()

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
        if node.node_type == graph.NODE_TYPE.TERMINAL_NODE:
            node.update_value()

def reset_values(nodes):
    for _, node in nodes.items():
        if node.node_type != graph.NODE_TYPE.TERMINAL_NODE:
            node.value = 0

def update_policies(nodes):
    policy_updated = False
    for _, node in nodes.items():
        if node.node_type == graph.NODE_TYPE.DECISION_NODE:
            policy_updated = node.update_policy() or policy_updated
    if policy_updated:
        reset_values(nodes)
    return policy_updated

def value_iteration(nodes):
    carry_over_values(nodes)
    nodes[next(iter(nodes))].within_tolerance = False
    iter_count = 0
    while (iter_count < graph.CONSTANTS.iteration_limit and not check_if_within_tolerance(nodes)):
        one_value_iteration(nodes)
        carry_over_values(nodes)
        iter_count += 1
    return update_policies(nodes)

def generic_markov_solver(nodes):
    set_chance_nodes_probabilities(nodes)
    assert_proper_input(nodes)
    set_terminal_nodes(nodes)
    while(value_iteration(nodes)): pass

if __name__ == '__main__':
    nodes = init()
    generic_markov_solver(nodes)
    print_policies(nodes)
    print_values(nodes)
