# CSCI-GA.2560 Artificial Intelligence Lab 3 Generic Markov Solver

## Usage
markov_solver.py can be run by running the following command:  
```python3 markov_solver.py [-df DF] [-min] [-tol TOL] [-iter ITER] [-w [W]] input-file-path```

## Running Guide
Run the following command to get a description of all the positional and optional arguments:  
```python3 markov_solver.py -h```

Running the above command would give the following output:  
```
usage: markov_solver.py [-h] [-df DF] [-min] [-tol TOL] [-iter ITER] [-w [W]] input-file-path

CSCI-GA.2560 Artificial Intelligence Lab 3 Generic Markov Solver

positional arguments:
  input-file-path  positional argument that requires the input file path to be given

optional arguments:
  -h, --help       show this help message and exit
  -df DF           float discount factor [0, 1] to use on future rewards, default value = 1.0
  -min             optional argument to minimize values as costs; default value = False
  -tol TOL         argument to set float tolerance for exiting value iteration, default value = 0.001
  -iter ITER       argument to set the integer that indicates a cutoff for value iteration, default value = 100
  -w [W]           use this tag to write the output to file called 'output.out' in the same directory
```
Use the optional and postional arguments as needed.

## Testing
Note that testing was done on ```snappy1.cims.nyu.edu```