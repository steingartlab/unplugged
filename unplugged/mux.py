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

from unplugged import constants, docker
from unplugged.nodeforwarder import NodeForwarder


mux_: NodeForwarder = NodeForwarder(container=docker.mux)


@dataclass
class Channel:
    row: int
    module: int

    def __post_init__(self):
        if int(self.module) % 2 == 0:
            return

        print(f"Warning: {self.module=} is not even (for reference, {self.row=})")


def parse(command: str, module: int, row: int) -> str:
    return f"{command}{module},{row};{command}{int(module) + 1},{row};"


def execute(command: str, channel: Channel):
    offramp_row = channel.module if int(channel.module) < 6 else 6
    offramp_row = 1 if int(offramp_row) == 0 else offramp_row
    offramp = parse(
        command=command, module=constants.MUX_HIGHWAY, row=offramp_row
    )  # row=channel.module is not a mistake. We arrange the connections like this by design

    parsed = parse(command=command, module=channel.module, row=channel.row)
    payload = offramp + parsed
    mux_.write(payload=payload)


def clear():
    mux_.write(payload="C")


unlatch: Callable[[Channel], None] = partial(execute, command="U")
latch: Callable[[Channel], None] = partial(execute, command="L")
