from typing import List


class SimulationProperties:
    def __init__(self, source_lambdas: List[float], device_taus: List[float], buffer_capacity: int, max_requests: int):
        if len(source_lambdas) == 0:
            raise ValueError('assumed len(source_lambdas) > 0')
        if len(device_taus) == 0:
            raise ValueError('assumed len(device_taus) > 0')
        if buffer_capacity <= 0:
            raise ValueError(f'assumed buffer_capacity > 0, got {buffer_capacity}')
        if max_requests <= 0:
            raise ValueError(f'assumed max_requests > 0, got {max_requests}')
        self.source_lambdas = source_lambdas
        self.device_taus = device_taus
        self.buffer_capacity = buffer_capacity
        self.max_requests = max_requests
        self.num_sources = len(source_lambdas)
        self.num_devices = len(device_taus)


def default_properties() -> SimulationProperties:
    return SimulationProperties([1, 1, 1], [1, 1, 1], 3, 25000)
