Note that testing was done on ```snappy1.cims.nyu.edu```

lab2.py can be run by running the following command:  
```python3 learn.py [-h] -train TRAIN -test TEST [-K K] [-C C] [-v] [-w [W]] [-debug]```

Run the following command to get a description of all the positional and optional arguments:  
```python3 learn.py -h```

Running the above command would give the following output:  
```
usage: learn.py [-h] -train TRAIN -test TEST [-K K] [-C C] [-v] [-w [W]] [-debug]

CSCI-GA.2560 Artificial Intelligence Lab 4 Supervised Machine Learning: kNN and Naive Bayes

optional arguments:
  -h, --help    show this help message and exit
  -train TRAIN  pass path of training file
  -test TEST    pass path of testing file
  -K K          number of neighbors for kNN
  -C C          laplacian correction constant for Naive Bayes
  -v            use this tag to enable verbose output
  -w [W]        use this tag to write the output to file called 'output.log' in the same directory
  -debug        use this tag to enable debug mode
```
Use the optional and postional arguments as needed.