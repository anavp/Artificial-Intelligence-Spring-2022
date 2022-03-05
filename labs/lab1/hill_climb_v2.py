import json
import argparse
import copy
import random

class hillClimbingInterface:
    def getErrorValue():
        pass
    def getNeighbors():
        pass
    def getRandomState():
        pass
    def printCurrentState():
        pass
    def decideBetweenSimilar():
        pass
    def targetReached(self, state):
        return self.getErrorValue(state) == 0
    def printCurrentState(self, state, optMessage = ""):
        print(optMessage, end = "")
        if state == None:
            return
        if len(state) == 0:
            print("[]")
            return
        print("[", end = "")
        for each in state[:-1]:
            print(each, end = " ")
        print(state[-1], end = "] = ")
        print(self.getErrorValue(state))


class nQueensProblem(hillClimbingInterface):
    state = None
    boardSize = -1
    def __init__(self, boardSize):
        self.boardSize = boardSize
        self.state = [num for num in range(boardSize)]
    
    def getErrorValue(self, state):
        val = 0
        for row1, column1 in enumerate(state):
            for row2, column2 in enumerate(state):
                if row2 <= row1:
                    continue
                if row1 + column1 == row2 + column2 or row1 - column1 == row2 - column2:
                    val += 1
        return val
    
    def getNeighbors(self, state):
        neighbors = []
        for row1 in range(self.boardSize):
            for row2 in range(self.boardSize)[row1 + 1:]:
                curCopy = copy.deepcopy(state)
                curCopy[row1], curCopy[row2] = curCopy[row2], curCopy[row1]
                neighbors.append(curCopy)
        return neighbors

    def getRandomState(self):
        random.shuffle(self.state)
        return self.state
    
    def decideBetweenSimilar(self, states, alreadyVisited = []):
        for each in alreadyVisited:
            if each in states:
                states.remove(each)
        if len(states) > 0:
            return states[random.randint(0, len(states) - 1)]
        else:
            return None

class knapsackProblem(hillClimbingInterface):
    T, M = 0, 0
    state = {}
    objectsDict = {}
    def __init__(self, filename):
        filename = open(filename)
        file = json.load(filename)
        self.T, self.M = file['T'], file['M']
        for each in file['Items']:
            self.objectsDict[each['name']] = (each['name'], each['V'], each['W'])
        self.state = file['Start']
        pass
    
    def getErrorValue(self, state):
        totalVal, totalWeight = 0, 0
        for each in state:
            _, curVal, curWeight = self.objectsDict[each]
            totalVal += curVal
            totalWeight += curWeight
        return max(totalWeight - self.M, 0) + max(self.T - totalVal, 0)
    
    def getNeighbors(self, state):
        neighbors = []

        # Add and subtract
        for each in self.objectsDict.keys():
            curCopy = copy.deepcopy(state)
            if each in state:
                curCopy.remove(each)
            else:
                curCopy.append(each)
            curCopy.sort()
            neighbors.append(curCopy)
        
        # Swap
        for each in state:
            for each2 in self.objectsDict.keys():
                curCopy = copy.deepcopy(state)
                curCopy.remove(each)
                if each2 in state:
                    continue
                curCopy.append(each2)
                curCopy.sort()
                neighbors.append(curCopy)
        return neighbors

    def getRandomState(self):
        self.state = random.sample(self.objectsDict.keys(), random.randint(1, len(self.objectsDict.keys())))
        self.state.sort()
        return self.state

    # higher value followed by lower weight
    def decideBetweenSimilar(self, states, alreadyVisited = []):
        highVal, minWeight = -1, -1
        selState = None
        for state in states:
            if state in alreadyVisited:
                continue
            totalVal, totalWeight = 0, 0
            for each in state:
                _, curVal, curWeight = self.objectsDict[each]
                totalVal += curVal
                totalWeight += curWeight
            if totalVal > highVal:
                highVal = totalVal
                minWeight = totalWeight
                selState = state
            elif totalVal == highVal and totalWeight < minWeight:
                minWeight = totalWeight
                selState = state
        return selState

    

def getMin(states, funcs, v):
    errorFunc, printFunc = funcs
    minVal = -1
    state = [states[0]]
    for each in states:
        if v:
            printFunc(each)
        curVal = errorFunc(each)
        if minVal == -1 or minVal > curVal:
            state = [each]
            minVal = curVal
        elif minVal == curVal:
            state.append(each)
    return state

def doHillClimbing(hObj, v, maxSideSteps, maxRestarts):
    state = hObj.state
    hObj.printCurrentState(state, "Start: ")
    sideStepsTaken = 0
    restartsDone = 0
    alreadyVisited = [state]

    while not hObj.targetReached(state):
        newStates = getMin(hObj.getNeighbors(state), (hObj.getErrorValue, hObj.printCurrentState), v)
        newError = hObj.getErrorValue(newStates[0])
        error = hObj.getErrorValue(state)
        if error < newError:
            restartsDone += 1
            if restartsDone > maxRestarts:
                hObj.printCurrentState(None, "not found\n")
                break
            else:
                state = hObj.getRandomState()
                hObj.printCurrentState(state, "restarting with: ")
                alreadyVisited = [state]
        elif error == newError:
            sideStepsTaken += 1
            newState = hObj.decideBetweenSimilar(newStates, alreadyVisited)
            if newState == None or sideStepsTaken > maxSideSteps:
                restartsDone += 1
                if restartsDone > maxRestarts:
                    hObj.printCurrentState(None, "not found\n")
                    break
                else:
                    state = hObj.getRandomState()
                    hObj.printCurrentState(state, "restarting with: ")
                    alreadyVisited = [state]
                    sideStepsTaken = 0
                    continue
            state = newState
            hObj.printCurrentState(state, "choose(sideways): ")
            alreadyVisited.append(state)
            pass
        else:
            state = newStates[0]
            hObj.printCurrentState(state, "choose: ")
            alreadyVisited = [state]
    if hObj.getErrorValue(state) == 0:
        hObj.printCurrentState(state, "Goal: ")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Hill Climbing")
    parser.add_argument("file", type = str, nargs = '?', default="Not Defined", help = "knapsack file input")
    parser.add_argument("-N", type = int, required = False, default = -1, help = "NQueens board size")
    parser.add_argument("-v", required = False, default = False, action = 'store_true',\
        help = "use this tag to generate the verbose output")
    parser.add_argument("-maxSidewaysSteps", type = int, required = False, default = 0, help = "maximum sideways steps count")
    parser.add_argument("-maxRestarts", type = int, required = False, default = 0, help = "number of restarts allowed")
    args = parser.parse_args() 
    if args.file == "Not Defined":
        hObj = nQueensProblem(args.N)
    else:
        hObj = knapsackProblem(args.file)
    doHillClimbing(hObj, args.v, args.maxSidewaysSteps, args.maxRestarts)

