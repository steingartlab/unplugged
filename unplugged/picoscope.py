"""Interface with oscilloscopes from PicoTech, called picoscopes."""

from dataclasses import asdict, dataclass
import json
from typing import Dict, List

import requests

from unplugged import constants, docker


URL: str = f'http://{constants.NETWORK_IP}.{str(docker.picoscope.ip_ending)}:{str(docker.picoscope.port)}/get_wave'


@dataclass#(kw_only) <- TODO: Implement when py3.10
class Picoscope:
    """All the params that should should be passed
    to a pulsing picoscope, no more, no less.

    Change at your leisure.
    """

    delay: float
    duration: float
    voltage_range: float
    avg_num: int = 64


def callback(pulsing_params: Picoscope) -> Dict[str, List[float]]:
    """Queries data from oscilloscope.
    
    Args:
        pulsing_params (Picoscope): See Picoscope.
        
    Returns:
        dict[str: list[float]]: Single key-value pair with key='data' and value
            acoustics pulse data.
    """

    response = requests.post(URL, data=asdict(pulsing_params)).text
    
    return json.loads(response) 
