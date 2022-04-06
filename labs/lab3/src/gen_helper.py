import graph

DEBUG_MODE = False

def create_node_if_not_exist(node_dict, node_name):
    if node_name not in node_dict.keys():
        node_dict[node_name] = graph.node(node_name)
    return node_dict