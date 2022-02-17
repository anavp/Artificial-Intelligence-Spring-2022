from helper import *

DEBUG_MODE = True





if __name__ == '__main__':
    args = parse_args()

    if (DEBUG_MODE):
        print("--verbose: " + str(args.verbose))
        print("--sideways: " + str(args.sideways))
        print("--restarts: " + str(args.restarts))