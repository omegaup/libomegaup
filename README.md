# omegaUp

Library for interacting with omegaUp.

## `omegaup.validator.validatortest`

Allows a validator to be modeled as a standard unit test.

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
    original_input = open('data.in', 'r')
    original_output = open('data.out', 'r')

    logging.info('This will be printed to stderr')

    self.assertAlmostEqual(float(contestant_output.readline().strip()),
                           float(original_output.readline().strip()))


if __name__ == '__main__':
    validatortest.main()
```
