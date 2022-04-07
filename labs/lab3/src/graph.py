import random
# import io_helper
# from io_helper import static_vars
import io_helper
from enum import Enum
import gen_helper

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
    if gen_helper.DEBUG_MODE:
        neighbor_values = dict()
    
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
        if gen_helper.DEBUG_MODE:
            self.neighbor_values = dict()
    
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
        if gen_helper.DEBUG_MODE:
            self.neighbor_values = dict()

    def add_neighbor(self, neighbor):
        self.neighbors[neighbor.name] = (self.__neighbor_object(self.__neighbor_count, neighbor))
        self.neighbor_list.append(neighbor.name)
        self.__neighbor_count += 1
    
    def set_arbitrary_policy(self):
        # self.__policy = 0
        self.__policy = random.randint(0, len(self.neighbors) - 1)
        self.policy_name = self.neighbor_list[self.__policy]
    
    def set_probabilities_by_alpha(self):
        assert self.__policy is not None and self.policy_name is not None
        assert self.node_type == NODE_TYPE.DECISION_NODE
        self.neighbors[self.policy_name].probability = 1 - self.alpha
        sum = 1 - self.alpha
        if len(self.neighbor_list) == 1:
            assert sum == 1
            return
        value = float(self.alpha) / float(len(self.neighbor_list) - 1)
        for neighbor in self.neighbor_list:
            if neighbor == self.policy_name:
                continue
            self.neighbors[neighbor].probability = value
            sum += value
        assert sum == 1
    
    def set_chance_node_probabilities(self):
        assert self.node_type == NODE_TYPE.CHANCE_NODE
        value = 1.0 / float(len(self.neighbor_list))
        for neighbor, neighbor_obj in self.neighbors.items():
            if neighbor_obj.probability is not None:
                return
            neighbor_obj.probability = value
    
    def better_value(self, value, max_value):
        if not CONSTANTS.minimize:
            return value > max_value
        return value < max_value

    def update_policy(self):
        assert self.node_type == NODE_TYPE.DECISION_NODE
        new_policy, value = 0, 0
        max_value = float('-inf') if not CONSTANTS.minimize else float('inf')
        assert len(self.neighbor_list) > 0
        if len(self.neighbor_list) > 1:
            alpha_rest = float(self.alpha) / float(len(self.neighbor_list) - 1)
        else:
            alpha_rest = 0
        
        for neighbor in self.neighbor_list:
            neighbor_obj = self.neighbors[neighbor]
            value = (float(1-self.alpha) * neighbor_obj.neighbor.value)
            for neighbor2 in self.neighbor_list:
                if neighbor2 == neighbor:
                    continue
                neighbor_obj = self.neighbors[neighbor2]
                value += (alpha_rest * neighbor_obj.neighbor.value)
            value *= CONSTANTS.discount_factor
            value += self.reward
            if gen_helper.DEBUG_MODE:
                self.neighbor_values[neighbor] = value
            if self.better_value(value, max_value):
                max_value = value
                new_policy = neighbor
        self.__policy = self.neighbor_list.index(new_policy)
        policy_updated = (self.policy_name != new_policy)
        self.policy_name = new_policy
        self.set_probabilities_by_alpha()
        return policy_updated
    
    def update_value(self):
        if self.node_type == NODE_TYPE.TERMINAL_NODE:
            self.value = self.reward
            return
        value = 0
        for neighbor in self.neighbor_list:
            neighbor_obj = self.neighbors[neighbor]
            assert neighbor_obj.probability is not None, self.name + "; " + neighbor
            value += neighbor_obj.neighbor.prev_value * neighbor_obj.probability
        value *= CONSTANTS.discount_factor
        value += self.reward
        self.value = value

    def carry_over_value(self):
        self.within_tolerance = (abs(self.value - self.prev_value) <= CONSTANTS.tolerance)
        self.prev_value = self.value
    
    def assert_proper_input(self):
        if self.node_type != NODE_TYPE.DECISION_NODE:
            return
        assert len(self.neighbor_list) > 1 or self.alpha == 0, "The number of edges can'1 be 1 and alpha != 0"

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
        if gen_helper.DEBUG_MODE:
            io_helper.print_func("policy possibilities:")
            for neighbor, value in self.neighbor_values.items():
                io_helper.print_func(neighbor + ' : %.3f'%value)

        io_helper.print_func("neighbor count: " + str(self.__neighbor_count))
        io_helper.print_func("neighbors:")
        for neighbor in self.neighbor_list:
            io_helper.print_func("neighbor name: " + neighbor)
            io_helper.print_func("neighbor probability: " + '%.3f'%(self.neighbors[neighbor].probability))
        io_helper.print_func("node end\n")