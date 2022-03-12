Note that testing was done on ```snappy1.cims.nyu.edu```

lab2.py can be run by running the following command:  
```python3 lab2.py [-h] [-v] -mode MODE mode_file_path [-w]```

Run the following command to get a description of all the positional and optional arguments:  
```python3 lab2.py -h```

Running the above command would give the following output:  
```
usage: lab2.py [-h] [-v] -mode MODE [-w] mode_file_path

CSCI-GA.2560 Artificial Intelligence Lab2 BNF to CNF and DPLL solver code

positional arguments:
  mode_file_path  pass the path of the mode's input file

optional arguments:
  -h, --help      show this help message and exit
  -v              use this tag to generate the verbose output
  -mode MODE      mode can be one of 'cnf', 'dpll', or 'solver'
  -w              use this tag to write the output to file called 
                  'output.out' in the same directory
```
Use the optional and postional arguments as needed.