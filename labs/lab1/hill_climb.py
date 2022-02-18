from distutils.debug import DEBUG
from helper import *

DEBUG_MODE = False


def getNeighbors(state):
    return None


def basicHillClimbing(initial, goal, actions, h):
    print(actions(initial))
    return
    state = initial
    while not goal(state):
      neighbors = []
    #   for s in actions(state):
    #     heapq.heappush(neighbors, (h(s), s))
    #   if neighbors[0][0] <= h(state):
    #     raise Error("unable to improve from %s" % s)
      state = neighbors[0][1]
    return state


def processHillClimbing(obj, verbose, sideways, restarts):
    basicHillClimbing(obj.state, obj.goal, obj.actions, obj.computeError)


if __name__ == '__main__':
    args = parse_args()
    
    verifyIfGoodArgumentsGiven(args)
    assertThatTheClassIsGood()

    if (DEBUG_MODE):
        print_args(args)

    if args.N == -1:
        obj = knapsackState(args.knapsackFile)
        if DEBUG_MODE:
            obj.printAllObjects()
    else:
        obj = nQueensState(args.N)
        if DEBUG_MODE:
            obj.printNumOfQueens()

    processHillClimbing(obj, args.verbose, args.sideways, args.restarts)