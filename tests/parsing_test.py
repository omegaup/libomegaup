#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Test omegaup.validator.validatortest."""

import unittest
import parsy as p  # type: ignore

import omegaup.validator.parsing as oup


class TestValidatorParsing(unittest.TestCase):
    """Test omegaup.validator.parsing."""
    def test(self) -> None:
        """Basic test."""
        self.assertEqual(oup.integer.parse('-1234'), -1234)
        self.assertEqual(oup.natural.parse('1234'), 1234)
        self.assertRaises(p.ParseError,
                          lambda: oup.boundInteger(0, 1).parse("2"))


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
