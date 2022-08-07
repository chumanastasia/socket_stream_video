from dataclasses import dataclass


@dataclass(frozen=True)
class ServerData:
    frame: bytes
    random_array: tuple
