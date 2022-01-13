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


class TestRunnerV2(unittest.TextTestRunner):
    """A unittest.TestRunner that prints 1 on standard output on success.
    If the associated .out file has contents, the test will consider
    it to be the expected failure message for the case and will fail
    with JE instead of WA. This is useful for invalid-inputs-enabled
    CI runs."""

    def run(self,
            test: Union[unittest.suite.TestSuite, unittest.case.TestCase]
            ) -> unittest.result.TestResult:
        result = super().run(test)
        if result is not None:
            if result.wasSuccessful():
                print(1)
            else:
                # Check if we asserted what we expected.
                with open('data.out', 'r') as file:
                    expectedError = file.read().strip()

                errorMatched = True
                for (_, errorString) in result.failures:
                    if expectedError not in errorString:
                        errorMatched = False

                if errorMatched and not result.errors:
                    print(0)
                else:
                    print("FAIL")
                    logging.error("Unexpected veredict failure: "
                                  "refusing to score case.\n"
                                  "Expected: %s", expectedError)
        return result


def main(testRunnerVersion: int = 1) -> None:
    """Executes the tests on the current file."""
    logging.basicConfig(level=logging.DEBUG)

    if testRunnerVersion == 1:
        unittest.main(testRunner=TestRunner, argv=[sys.argv[0], '-v'])
    else:
        unittest.main(testRunner=TestRunnerV2, argv=[sys.argv[0], '-v'])
