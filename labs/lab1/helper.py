import argparse


def parse_args(args = None):
    parser = argparse.ArgumentParser(description="Hill climbing code for AI course")
    parser.add_argument("-verbose", type = bool, required = False, default = False,\
        help = "verbose flag somethign something")#TODO: write better description
    parser.add_argument("-sideways", type = int, required = False, default = 0, \
        help = "put the count of sideways steps allowed; default value = 0")
    parser.add_argument("-restarts", type = int, required = False, default = 0, \
        help = "the number of random restarts allowed; default = 0")
    return parser.parse_args()