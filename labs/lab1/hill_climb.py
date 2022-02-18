from helper import *
from random import shuffle

DEBUG_MODE = False

# TODO: Tie breakers
# TODO: maintain a visited list to avoid sideways cycles
# TODO: Queens, knapsack, hill climbing???????
# TODO: interface methods: value, next, restart, print
# TODO: enabling of sideways somehow randomizes the neigbors selection for bethe. Figure out what's happening

def moveSidewaysOrRestart(sCounter, rCounter, maxSteps, maxRestarts, sPossible, sIndex, neighbors, state, h):
    if sPossible and sCounter < maxSteps:
        sCounter += 1
        state = neighbors[sIndex]
        write("choose(sideways): ", end = "")
        writeState(state, h(state))
    elif rCounter < maxRestarts:
        shuffle(state)
        rCounter += 1
        write("restarting with: ", end = "")
        writeState(state, h(state))
    else:
        write("not found")
        exit(0)
    return state, sCounter, rCounter


def hillClimbing(initial, goal, actions, h, verbose, maxSteps, maxRestarts):
    write("Start: ", end = "")
    writeState(initial, h(initial))
    state = initial
    sCounter = 0
    rCounter = 0

    while not goal(state):
        neighbors = actions(state)
        minError = h(state)
        minErrorIndex = -1
        sPossible = False
        sIndex = -1
        for index, s in enumerate(neighbors):
            currentError = h(s)
            if verbose:
                writeState(s, currentError)
            if currentError < minError:
                minError = currentError
                minErrorIndex = index
            elif not sPossible and currentError == minError:
                sPossible = True
                sIndex = index
        if minErrorIndex == -1:
            state, sCounter, rCounter = moveSidewaysOrRestart(sCounter, rCounter, maxSteps, maxRestarts, sPossible, sIndex, neighbors, state, h)
        else:
            state = neighbors[minErrorIndex]
            sCounter = 0
            write("choose: ", end = "")
            writeState(state, minError)
    write("Goal: ", end = "")
    writeState(state, h(state))


if __name__ == '__main__':
    args = parse_args()
    
    verifyIfGoodArgumentsGiven(args)
    assertThatTheClassIsGood()

    if (DEBUG_MODE):
        print_args(args)

    obj = getObject(args)

    if DEBUG_MODE:
        obj.printThings()
    
    hillClimbing(obj.state, obj.goal, obj.Next, obj.Value, args.verbose, args.sideways, args.restarts)