import random
import io_helper

class node:
    name = None
    reward = None
    alpha = None
    __policy = None
    policy_name = None
    __neighbor_count = None
    neighbors = {}
    neighbor_list = []
    
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
    
    def __init__(self, name):
        self.name = name
        self.alpha = 0
        self.reward = 0
        self.__neighbor_count = 0
        self.__policy = None
        self.neighbors = dict()
        self.neighbor_list = list()
        self.policy_name = None

    def add_neighbor(self, neighbor):
        self.neighbors[neighbor.name] = (self.__neighbor_object(self.__neighbor_count, neighbor))
        self.neighbor_list.append(neighbor.name)
        self.__neighbor_count += 1
    
    def set_arbitrary_policy(self):
        self.__policy = random.randint(0, len(self.neighbors) - 1)
        self.policy_name = self.neighbor_list[self.__policy]
    
    def set_probabilities_by_alpha(self):
        assert self.__policy is not None and self.policy_name is not None
        assert self.neighbors[self.policy_name].probability is None
        self.neighbors[self.policy_name].probability = 1 - self.alpha
        sum = 1 - self.alpha
        value = float(self.alpha) / float(len(self.neighbor_list) - 1)
        for neighbor in self.neighbor_list:
            if neighbor == self.policy_name:
                continue
            assert self.neighbors[neighbor].probability is None
            self.neighbors[neighbor].probability = value
            sum += value
        assert sum == 1
    
    def update_policy(self):
        # TODO: Write this
        pass
    
    def print_node(self):
        io_helper.print_func("name: " + self.name)
        io_helper.print_func("reward: " + str(self.reward))
        io_helper.print_func("alpha: " + str(self.alpha))
        io_helper.print_func("policy: ", end = '')
        if self.policy_name is not None:
            io_helper.print_func(self.policy_name)
        else:
            io_helper.print_func("None")
        io_helper.print_func("neighbor count: " + str(self.__neighbor_count))
        io_helper.print_func("neighbors:")
        for neighbor in self.neighbor_list:
            io_helper.print_func("neighbor name: " + neighbor)
            io_helper.print_func("neighbor probability: " + str(self.neighbors[neighbor].probability))
        io_helper.print_func("node end\n")