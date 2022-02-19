Note that testing was done on ```snappy1.cims.nyu.edu```

hill_climb.py can be run by running the following command:  
```python3 hill_climb.py [-h] [-N N] [-verbose] [-sideways [SIDEWAYS]] [-restarts RESTARTS] [-w] [knapsack-file-path]```

Run the following command to get a description of all the positional and optional arguments:  
```python3 hill_climb.py -h```

Running the above command would give the following output:  
```
usage: hill_climb.py [-h] [-N N] [-verbose] [-sideways [SIDEWAYS]]
                     [-restarts RESTARTS] [-w]
                     [knapsack-file-path]

CSCI-GA.2560 Artificial Intelligence Lab1 Hill Climbing Code

positional arguments:
  knapsack-file-path    pass the path of the knapsack input file

optional arguments:
  -h, --help            show this help message and exit
  -N N                  the number of queens in the N-Queens problem
  -verbose              use this tag to generate the verbose output
  -sideways [SIDEWAYS]  the number of sideways steps allowed; default = 0
  -restarts RESTARTS    the number of random restarts allowed; default = 0
  -w                    use this tag to write the output to file called
                        'output.out' in the same directory
```
Use the optional and postional arguments as needed.
