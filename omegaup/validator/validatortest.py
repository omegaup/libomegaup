# -*- coding: utf-8 -*-
"""Allows a validator to be modeled as a standard unit test.

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
"""

import logging
import sys
import unittest
import unittest.case
import unittest.suite

from typing import Union


class TestRunner(unittest.TextTestRunner):
    """A unittest.TestRunner that prints 1 on standard output on success."""
    def run(
        self, test: Union[unittest.suite.TestSuite, unittest.case.TestCase]
    ) -> unittest.result.TestResult:
        result = super().run(test)
        if result is not None and result.wasSuccessful():
            print(1)
        else:
            print(0)
        return result


def main() -> None:
    """Executes the tests on the current file."""
    logging.basicConfig(level=logging.DEBUG)
    unittest.main(testRunner=TestRunner, argv=[sys.argv[0], '-v'])
