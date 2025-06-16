# pyright: reportAny=false
from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from textwrap import wrap
from typing import Any

from pydantic import BaseModel


def logfmt(value: Any) -> str: ...


# FIX:
def pretty(value: Any, tabs: int) -> str:
    MAX_WIDTH = 80
    pad = '\t' * tabs

    match value:
        case BaseModel():
            # if type(value).__str__ is not SpaceTradersAPIResShape.__str__:
            #     return str(value)
            lines = [f'{pad}{value.__class__.__name__}']
            for k, v in value.__dict__.items():
                lines.append(f'{pad}\t{k}: {pretty(v, tabs + 1).lstrip()}')
            return '\n'.join(lines)

        case list():
            if not value:
                return '[]'
            inline = f'[{", ".join(pretty(v, tabs) for v in value)}]'

            if len(inline) <= MAX_WIDTH:
                return inline

            return '[\n' + '\n'.join(pretty(v, tabs + 1) for v in value) + f'\n{pad}]'

        case datetime():
            return value.strftime('%Y-%m-%d %H:%M:%S')

        case date():
            return value.strftime('%Y-%m-%d')

        case Enum():
            return value.name

        case str():
            if len(value) > MAX_WIDTH:
                return '...' + ''.join(f'\n{pad}\t{line}' for line in wrap(value, width=MAX_WIDTH))

            return value

        case _:
            return repr(value)
