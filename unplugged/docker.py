"""Container metadata. Everything in here must
match the docker-compose.yaml file. Yes, we should
autosync it but whatever.
"""

from dataclasses import dataclass


@dataclass
class Container:
    ip_ending: int
    port: int

mux = Container(ip_ending=21, port=9020)
picoscope = Container(ip_ending=10, port=5001)
pulser = Container(ip_ending=11, port=9002)
unplugged = Container(ip_ending=0, port=9001)
