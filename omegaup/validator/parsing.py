# -*- coding: utf-8 -*-
"""Parsing helpers
"""

import parsy as p   # type: ignore

from typing import Any, Optional

space = p.string(" ").desc("space")
eol = p.string("\n").desc("eol")
integer = p.regex("-?[0-9]+").map(int).desc("integer")


def boundInteger(min: Optional[int], max: Optional[int]) -> Any:
    @p.generate(f"integer between {min} and {max}")  # type: ignore
    def parser() -> Any:
        num = yield integer
        if min is not None and not min <= num:
            return p.fail('out of bounds')
        if max is not None and not num <= max:
            return p.fail('out of bounds')
        return num

    return parser


natural = boundInteger(0, None).desc("natural number")
