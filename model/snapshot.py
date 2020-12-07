from model.buffer import BufferState
from model.stats import Stats

from enum import Enum, auto
from typing import List, Optional


class SimulationEvent(Enum):
    REQUEST_GENERATED = auto()
    REQUEST_HANDLED = auto()
    DEVICE_PAUSED = auto()
    REQUEST_HANDLED_IMMEDIATE = auto()


class Snapshot:
    def __init__(self, time: float, event_type: SimulationEvent,
                 actor: int, buffer_state: BufferState,
                 device_requests: List[Optional[int]], stats: Stats,
                 actor2: Optional[int] = None):
        self.time = time
        self.event_type = event_type
        self.actor = actor
        self.buffer_state = buffer_state
        self.device_requests = device_requests
        self.stats = stats
        self.actor2 = actor2

    def __str__(self):
        s = f'{self.time} : {self.event_type.name} by {self.actor}'
        if self.actor2 is not None:
            s += f' from {self.actor2}'
        s += f'\n{self.buffer_state}'
        return s
