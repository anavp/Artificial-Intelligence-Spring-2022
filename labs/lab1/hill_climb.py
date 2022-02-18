from distutils.debug import DEBUG
from helper import *

DEBUG_MODE = False


def basicHillClimbing(initial, goal, actions, h, verbose):
    initial.sort()
    write("Start: ", end = "")
    writeState(initial, h(initial))
    state = initial
    while not goal(state):
        neighbors = actions(state)
        minError = h(state)
        minErrorIndex = -1
        for index, s in enumerate(neighbors):
            currentError = h(s)
            if verbose:
                s.sort()
                writeState(s, currentError)
            if currentError < minError:
                minError = currentError
                minErrorIndex = index
        if minErrorIndex == -1:
            write("Unable to improve from ", end = "")
            writeState(state, h(state))
            return state
        else:
            state = neighbors[minErrorIndex]
            state.sort()
            write("choose: ", end = "")
            writeState(state, minError)
    return state


def processHillClimbing(obj, verbose, sideways, restarts):
    goal = basicHillClimbing(obj.state, obj.goal, obj.actions, obj.computeError, verbose)
    write("Goal: ", end = "")
    writeState(goal, obj.computeError(goal))


if __name__ == '__main__':
    args = parse_args()
    
    verifyIfGoodArgumentsGiven(args)
    assertThatTheClassIsGood()

    if (DEBUG_MODE):
        print_args(args)

    obj = getObject(args)

    if DEBUG_MODE:
        obj.printThings()
    processHillClimbing(obj, args.verbose, args.sideways, args.restarts)