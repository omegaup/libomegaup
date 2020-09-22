# omegaUp

Library for interacting with omegaUp.

## `omegaup.validator.validatortest`

Allows an input validator to be modeled as a standard unit test.

To use, write your validator as if it were a normal
[unittest.TestCase](https://docs.python.org/3/library/unittest.html#unittest.TestCase):

```python
import logging
import unittest
import sys

from omegaup.validator import validatortest


class MyTest(unittest.TestCase):
  def test_foo(self):
    contestant_output = sys.stdin
    case_name = sys.argv[1]
    with open('data.in', 'r') as original_input, \
         open('data.out', 'r') as original_output:
        logging.info('This will be printed to stderr')

        self.assertAlmostEqual(
            float(contestant_output.readline().strip()),
            float(original_output.readline().strip()))


if __name__ == '__main__':
    validatortest.main()
```
