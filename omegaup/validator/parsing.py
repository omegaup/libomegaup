# -*- coding: utf-8 -*-
"""Parsing helpers
"""

import parsy as p   # type: ignore

from typing import Union, Any

space = p.regex(" ").desc("space")
eol = p.regex("\n").desc("eol")
integer = p.regex("-?[0-9]+").map(int).desc("integer")


def boundInteger(min: int, max: int) -> Any:
    @p.generate(f"integer between {min} and {max}")  # type: ignore
    def parser() -> Union[int, Any]:
        num = yield integer
        if not min <= num <= max:
            return p.fail('out of bounds')
        return num

    return parser
