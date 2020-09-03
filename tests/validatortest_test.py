#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Test omegaup.validator.validatortest."""

import unittest

from omegaup.validator import validatortest


@unittest.skipUnless(__name__ == '__main__', 'needs to be run by itself')
class TestValidatorTest(unittest.TestCase):
    """Test omegaup.validator.validatortest."""
    def test(self) -> None:
        """Basic test."""
        self.assertTrue(True)


if __name__ == '__main__':
    validatortest.main()

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
