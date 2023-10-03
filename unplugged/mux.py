"""Interface with Cytec CXAR/128 multiplexer.
Well, it probably works for other Cytec models as wells.
"""

from dataclasses import dataclass
from functools import partial
from typing import Callable

from unplugged import docker
from unplugged.nodeforwarder import NodeForwarder


mux_: NodeForwarder = NodeForwarder(container=docker.mux)


@dataclass
class Channel:
    row: int
    modules: tuple[int, int] = (0, 1)


def parse(command: str, modules: tuple[int, int], row: int) -> str:
    return f'{command}{modules[0]},{row};{command}{modules[1]}{row};'


def execute(command: str, channel: Channel):
    parsed = parse(command=command, modules=channel.modules, row=channel.row)
    mux_.write(payload=parsed)

def clear():
    mux_.write(payload='C')


unlatch: Callable[[Channel], None] = partial(execute, command='U')
latch: Callable[[Channel], None] = partial(execute, command='L')
