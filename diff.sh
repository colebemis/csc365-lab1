#!/bin/bash

for test_input in *.in; do
   # strip off the file extension, i.e, the ".in"
   name=${test_input%.in}

   # run the test
   python3 lab1.py < $test_input 1> $name.out

   # diff the results
   diff -q $name.out $name.expect
done

