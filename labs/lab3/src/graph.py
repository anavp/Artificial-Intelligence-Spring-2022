import random
# import io_helper
# from io_helper import static_vars
import io_helper
from enum import Enum

def constants(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@constants(discount_factor = None, tolerance = None, iteration_limit = None, minimize = None)
class CONSTANTS:
    def __init__(self, df, tol, iter, min):
        CONSTANTS.discount_factor = df
        CONSTANTS.tolerance = tol
        CONSTANTS.iteration_limit = iter
        CONSTANTS.minimize = min

class NODE_TYPE(Enum):
    TERMINAL_NODE = 1
    CHANCE_NODE = 2
    DECISION_NODE = 3

class node:
    name = None
    reward = None
    alpha = None
    __policy = None
    policy_name = None
    __neighbor_count = None
    neighbors = {}
    neighbor_list = []
    value = 0
    prev_value = 0
    node_type = None
    within_tolerance = False
    
    class __neighbor_object:
        neighbor, probability, index = None, None, None
        def __init__(self, index, neighbor, probability = None):
            self.neighbor = neighbor
            self.probability = probability
            self.index = index
    
    def __init__(self, name, reward):
        self.name = name
        self.reward = reward
        self.alpha = 0
        self.__neighbor_count = 0
        self.__policy = None
        self.neighbors = dict()
        self.neighbor_list = list()
        self.policy_name = None
        self.value = 0
        self.node_type = NODE_TYPE.TERMINAL_NODE
        self.prev_value = 0
        self.within_tolerance = False
    
    def __init__(self, name):
        self.name = name
        self.alpha = 0
        self.reward = 0
        self.__neighbor_count = 0
        self.__policy = None
        self.neighbors = dict()
        self.neighbor_list = list()
        self.policy_name = None
        self.value = 0
        self.node_type = NODE_TYPE.TERMINAL_NODE
        self.prev_value = 0
        self.within_tolerance = False

    def add_neighbor(self, neighbor):
        self.neighbors[neighbor.name] = (self.__neighbor_object(self.__neighbor_count, neighbor))
        self.neighbor_list.append(neighbor.name)
        self.__neighbor_count += 1
    
    def set_arbitrary_policy(self):
        self.__policy = random.randint(0, len(self.neighbors) - 1)
        self.policy_name = self.neighbor_list[self.__policy]
    
    def set_probabilities_by_alpha(self):
        assert self.__policy is not None and self.policy_name is not None
        # assert self.neighbors[self.policy_name].probability is None
        self.neighbors[self.policy_name].probability = 1 - self.alpha
        sum = 1 - self.alpha
        value = float(self.alpha) / float(len(self.neighbor_list) - 1)
        for neighbor in self.neighbor_list:
            if neighbor == self.policy_name:
                continue
            # assert self.neighbors[neighbor].probability is None
            self.neighbors[neighbor].probability = value
            sum += value
        assert sum == 1
    
    def update_policy(self):
        assert self.node_type == NODE_TYPE.DECISION_NODE
        new_policy, value, max_value = 0, 0, float('-inf')
        assert len(self.neighbor_list) > 0
        alpha_rest = float(self.alpha) / float(len(self.neighbor_list) - 1)
        for neighbor in self.neighbor_list:
            neighbor_obj = self.neighbors[neighbor]
            value = (float(1-self.alpha) * neighbor_obj.neighbor.value)
            for neighbor2 in self.neighbor_list:
                if neighbor2 == neighbor:
                    continue
                neighbor_obj = self.neighbors[neighbor2]
                value += (alpha_rest * neighbor_obj.neighbor.value)
            if value > max_value:
                max_value = value
                new_policy = neighbor
        self.__policy = self.neighbor_list.index(new_policy)
        policy_updated = (self.policy_name != new_policy)
        self.policy_name = new_policy
        self.set_probabilities_by_alpha()
        return policy_updated
    
    def update_value(self):
        if self.node_type == NODE_TYPE.TERMINAL_NODE:
            self.prev_value = self.reward
            return
        # elif self.node_type == NODE_TYPE.CHANCE_NODE:
        value = 0
        for neighbor in self.neighbor_list:
            neighbor_obj = self.neighbors[neighbor]
            value += neighbor_obj.neighbor.prev_value * neighbor_obj.probability
        value *= CONSTANTS.discount_factor
        value += self.reward
        self.value = value
        # assert self.node_type == NODE_TYPE.DECISION_NODE

    def carry_over_value(self):
        self.within_tolerance = (abs(self.value - self.prev_value) <= CONSTANTS.tolerance)
        self.prev_value = self.value

    def print_node(self):
        io_helper.print_func("name: " + self.name)
        io_helper.print_func("value: " + '%.3f'%(self.value))
        io_helper.print_func("node_type: " + self.node_type.name)
        io_helper.print_func("reward: " + '%.3f'%(self.reward))
        io_helper.print_func("alpha: " + '%.3f'%(self.alpha))
        io_helper.print_func("policy: ", end = '')
        if self.policy_name is not None:
            io_helper.print_func(self.policy_name)
        else:
            io_helper.print_func("None")
        io_helper.print_func("neighbor count: " + str(self.__neighbor_count))
        io_helper.print_func("neighbors:")
        for neighbor in self.neighbor_list:
            io_helper.print_func("neighbor name: " + neighbor)
            io_helper.print_func("neighbor probability: " + '%.3f'%(self.neighbors[neighbor].probability))
        io_helper.print_func("node end\n")