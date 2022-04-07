#!/bin/bash

INPUTS=$(ls ../inputs/*.txt)
cd ../src/

python3 markov_solver.py ../inputs/hw8.txt -w ../outputs/hw8.out -df .9 -iter 150
python3 markov_solver.py ../inputs/maze.txt -w ../outputs/maze.out
python3 markov_solver.py ../inputs/publish.txt -w ../outputs/publish.out
python3 markov_solver.py ../inputs/restaurant.txt -min -w ../outputs/restaurant.out
python3 markov_solver.py ../inputs/student.txt -w ../outputs/student.out
python3 markov_solver.py ../inputs/student2.txt -w ../outputs/student2.out
python3 markov_solver.py ../inputs/teach.txt -df .9 -w ../outputs/teach.out

cd ../scripts/

python3 tester.py