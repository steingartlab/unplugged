"""Interface with Cytec CXAR/128 multiplexer.
Well, it probably works for other Cytec models as wells.

Plz read this header. We group every pulser/oscilloscope pair
with the same row numbers in adjacent modules, with the oscilloscope
(receiving transducer) being on an even number.

The center modules (4 & 5) are designated as the highway->offramp, i.e.
the pulser and picoscope are connected to there and the individual
jigs branch off from there. We do it so that the module 0/1 pair is connected
in row 0/1 on the highway (again, module 4 & 5), and so on. This simplifies
the mental overhead of the mux configuration, both physically and in code.
"""

from dataclasses import dataclass
from functools import partial
from typing import Callable

from unplugged import docker
from unplugged.nodeforwarder import NodeForwarder


mux_: NodeForwarder = NodeForwarder(container=docker.mux)
HIGHWAY = 4


@dataclass
class Channel:
    row: int
    module: int

    def __post_init__(self):
        if int(self.module) % 2 == 0:
            return

        print(f"Warning: {self.module=} is not even (for reference, {self.row=})")


def parse(command: str, module: int, row: int) -> str:
    return f"{command}{module},{row};{command}{module + 1},{row};"


def execute(command: str, channel: Channel):
    offramp = parse(
        command=command, module=HIGHWAY, row=channel.module
    )  # row=channel.module is not a mistake. We arrange the connections like this by design
    mux_.write(offramp)

    parsed = parse(command=command, module=channel.module, row=channel.row)
    mux_.write(parsed)


def clear():
    mux_.write(payload="C")


unlatch: Callable[[Channel], None] = partial(execute, command="U")
latch: Callable[[Channel], None] = partial(execute, command="L")
