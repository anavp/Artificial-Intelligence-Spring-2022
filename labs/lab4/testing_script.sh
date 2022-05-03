#!/bin/bash

python3 src/learn.py -train inputs/knn1.train.csv -test inputs/knn1.test.csv -K 3 -w output/knn1.e2.3.out.txt
python3 src/learn.py -train inputs/knn2.train.csv -test inputs/knn2.test.csv -K 3 -w output/knn2.e2.3.out.txt
python3 src/learn.py -train inputs/knn3.train.csv -test inputs/knn3.test.csv -K 3 -w output/knn3.e2.3.out.txt
python3 src/learn.py -train inputs/knn3.train.csv -test inputs/knn3.test.csv -K 5 -w output/knn3.e2.5.out.txt
python3 src/learn.py -train inputs/knn3.train.csv -test inputs/knn3.test.csv -K 7 -w output/knn3.e2.7.out.txt

python3 src/learn.py -train inputs/ex1_train.csv -test inputs/ex1_test.csv -C 0 -w output/nb1.0.out
python3 src/learn.py -train inputs/ex1_train.csv -test inputs/ex1_test.csv -C 0 -v -w output/nb1.0.v.out
python3 src/learn.py -train inputs/ex1_train.csv -test inputs/ex1_test.csv -C 1 -w output/nb1.1.out
python3 src/learn.py -train inputs/ex1_train.csv -test inputs/ex1_test.csv -C 1 -v -w output/nb1.1.v.out
python3 src/learn.py -train inputs/ex2_train.csv -test inputs/ex2_test.csv -C 0 -w output/nb2.0.out
python3 src/learn.py -train inputs/ex2_train.csv -test inputs/ex2_test.csv -C 0 -v -w output/nb2.0.v.out
python3 src/learn.py -train inputs/ex2_train.csv -test inputs/ex2_test.csv -C 1 -w output/nb2.1.out
python3 src/learn.py -train inputs/ex2_train.csv -test inputs/ex2_test.csv -C 1 -v -w output/nb2.1.v.out
python3 src/learn.py -train inputs/ex2_train.csv -test inputs/ex2_test.csv -C 2 -w output/nb2.2.out
python3 src/learn.py -train inputs/ex2_train.csv -test inputs/ex2_test.csv -C 2 -v -w output/nb2.2.v.out

diff refout/knn1.e2.3.out.txt output/knn1.e2.3.out.txt
diff refout/knn2.e2.3.out.txt output/knn2.e2.3.out.txt
diff refout/knn3.e2.3.out.txt output/knn3.e2.3.out.txt
diff refout/knn3.e2.5.out.txt output/knn3.e2.5.out.txt
diff refout/knn3.e2.7.out.txt output/knn3.e2.7.out.txt

diff refout/nb1.0.out output/nb1.0.out
diff refout/nb1.0.v.out output/nb1.0.v.out
diff refout/nb1.1.out output/nb1.1.out
diff refout/nb1.1.v.out output/nb1.1.v.out
diff refout/nb2.0.out output/nb2.0.out
diff refout/nb2.0.v.out output/nb2.0.v.out
diff refout/nb2.1.out output/nb2.1.out
diff refout/nb2.1.v.out output/nb2.1.v.out
diff refout/nb2.2.out output/nb2.2.out
diff refout/nb2.2.v.out output/nb2.2.v.out