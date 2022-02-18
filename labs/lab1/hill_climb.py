from helper import *

DEBUG_MODE = True


def getNeighbors(state):
    return None


def basicHillClimbing(initial, goal, actions, h):
    state = initial
    while not goal(state):
      neighbors = []
    #   for s in actions(state):
    #     heapq.heappush(neighbors, (h(s), s))
    #   if neighbors[0][0] <= h(state):
    #     raise Error("unable to improve from %s" % s)
      state = neighbors[0][1]
    return state


def processHillClimbing(verbose, sideways, restarts):
    print("doing hill climbing")


if __name__ == '__main__':
    args = parse_args()
    assert args.knapsackFile != "not_defined" or args.N > -1, "Either number of queens should be defined or a knapsack file must be passed"
    
    if (DEBUG_MODE):
        print_args(args)

    processHillClimbing(args.verbose, args.sideways, args.restarts)