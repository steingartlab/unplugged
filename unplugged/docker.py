"""Container metadata. Everything in here must
match the docker-compose.yaml file. Yes, we should
autosync it but whatever.
"""

from dataclasses import dataclass

BASE_IP: str = '192.168.0'


@dataclass
class Container:
    ip_ending: int
    port: int

mux = Container(ip_ending=21, port=9020)
printer = Container(ip_ending=22, port=9021)
picoscope = Container(ip_ending=10, port=5001)
pulser = Container(ip_ending=11, port=9002)
ustreamer = Container(ip_ending=14, port=8080)