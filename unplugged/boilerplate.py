from dataclasses import dataclass
from enum import Enum
from typing import Optional

from unplugged import mux, pulser
from unplugged.picoscope import Picoscope


class Status(Enum):
    idling = 0
    pulsing = 1
    running = 2


@dataclass
class Mode:
    """All configuration data that's unique to each mode,
    e.g. pulse/echo or transmission.
    """
    
    pulser: pulser.Pulser
    picoscope: Picoscope
    mux_channel: mux.Channel


@dataclass
class Jig:
    name: str
    status: Status
    mode: Mode
    exp_id: Optional[str] = None

    def __post_init__(self):
        self.status = Status[self.status]  # enforce typing


