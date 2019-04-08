#!/bin/bash

# Run this script to generate expected output files (.expect)
# from test cases (.in). Don't forget to double check the generated
# .expect files.

for test_input in *.in; do
  name=${test_input%.in}

  python3 lab1.py < $test_input > $name.expect
done
