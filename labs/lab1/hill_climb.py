from helper import *

DEBUG_MODE = False

# TODO: Tie breakers: done I think
# TODO: Queens, knapsack, hill climbing??????? There's no third case I think
# TODO: interface methods: value, next, restart, print: done
# TODO: maintain a visited list to avoid sideways cycles: done I think
# TODO: Bad input handling: argparsing does that automatically i think
# TODO: Fix tiebreaker : done
# TODO: enabling of sideways somehow randomizes the neigbors selection for bethe. Figure out what's happening: Prof is somehow not using tiebreakers when sideways = 0. I am not doing that
# TODO: Readme file


def moveSidewaysOrRestart(sCounter, rCounter, maxSteps, maxRestarts, sPossible, obj, visitedList, possibilities):
    if sPossible and sCounter < maxSteps:
        state = obj.tiebreaker(possibilities, visitedList)
        if state is None:
            pass
        else:
            sCounter += 1
            visitedList.append(state)
            obj.printState(state, "choose(sideways): ")
            return state, sCounter, rCounter, visitedList
    if rCounter < maxRestarts:
        state = obj.restart()
        rCounter += 1
        sCounter = 0
        visitedList = [state]
        obj.printState(state, "restarting with: ")
    else:
        obj.printState(prefix = "not found")
        exit(0)
    return state, sCounter, rCounter, visitedList


def hillClimbing(obj, verbose, maxSteps, maxRestarts):
    obj.printState(obj.state, "Start: ")
    state = obj.state
    sCounter = 0
    rCounter = 0
    visitedList = [state]

    while not obj.goal(state):
        neighbors = obj.next(state)
        minError = obj.value(state)
        minErrorIndex = -1
        sPossible = False
        possibilities = []

        for index, s in enumerate(neighbors):
            currentError = obj.value(s)
            if verbose:
                obj.printState(s)
            if currentError < minError:
                visitedList = [s]
                minError = currentError
                minErrorIndex = index
                possibilities = [s]
            elif not sPossible and currentError == minError and (s not in visitedList):
                sPossible = True
                possibilities.append(s)
            elif currentError == minError:
                possibilities.append(s)
        if minErrorIndex == -1:
            state, sCounter, rCounter, visitedList = moveSidewaysOrRestart(sCounter, rCounter, maxSteps, maxRestarts, sPossible, obj, visitedList, possibilities)
        else:
            if len(possibilities) == 1:
                state = neighbors[minErrorIndex]
            else:
                state = obj.tiebreaker(possibilities)
            sCounter = 0
            visitedList = [state]
            obj.printState(state, "choose: ")
    obj.printState(state, "Goal: ")


if __name__ == '__main__':
    args = parse_args()
    
    verifyIfGoodArgumentsGiven(args)
    assertThatTheClassIsGood()

    if (DEBUG_MODE):
        print_args(args)

    obj = getObject(args)

    if DEBUG_MODE:
        obj.printThings()
    
    hillClimbing(obj, args.verbose, args.sideways, args.restarts)