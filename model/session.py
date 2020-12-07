from model.device import Device
from model.buffer import Buffer
from model.generator import Generator
from model.stats import Stats
from model.snapshot import Snapshot, SimulationEvent
from model.properties import SimulationProperties

import logging


class Session:
    def __init__(self, properties: SimulationProperties):
        self.__stats = Stats(properties.num_sources, properties.num_devices)
        self.__generators = [Generator(i, l, self.__stats) for i, l in enumerate(properties.source_lambdas)]
        self.__devices = [Device(i, t, self.__stats) for i, t in enumerate(properties.device_taus)]
        self.__buffer = Buffer(properties.buffer_capacity, self.__stats)
        self.__max_requests = properties.max_requests
        self.__global_time = 0

    def __make_snapshot(self, event, actor, actor2=None) -> Snapshot:
        logging.debug(f'buffer : {self.__buffer}')
        logging.debug(f'handled : {self.__stats.total_handled}')
        logging.debug(f'rejected : {self.__stats.total_rejected}')
        logging.debug(f'devices : {" ".join(map(lambda device: "P" if device.paused else "W", self.__devices))}\n')
        return Snapshot(
            self.__global_time,
            event,
            actor,
            self.__buffer.state,
            list(map(lambda device: device.current_request_source, self.__devices)),
            self.__stats,
            actor2=actor2
        )

    @property
    def done(self):
        return self.__stats.total_handled > self.__max_requests

    def run(self, on_step=lambda _: None) -> Stats:
        while not self.done:
            on_step(self.step())
        self.__stats.simulation_ended(self.__global_time)
        return self.__stats

    def step(self) -> Snapshot:
        nearest_generator = min(self.__generators, key=lambda generator: generator.new_request_time)
        nearest_device = min(
            filter(lambda device: not device.paused, self.__devices),
            key=lambda device: device.available_at,
            default=None
        )
        if nearest_device is None or nearest_generator.new_request_time <= nearest_device.available_at:
            self.__global_time = nearest_generator.new_request_time
            new_request = nearest_generator.generate()
            paused_devices = list(filter(lambda device: device.paused, self.__devices))
            if len(paused_devices) > 0:
                new_request.left_buffer = self.__global_time
                paused_devices[0].handle(new_request)
                return self.__make_snapshot(SimulationEvent.REQUEST_HANDLED_IMMEDIATE, paused_devices[0].device_id,
                                            nearest_generator.generator_id)
            self.__buffer.insert(new_request)
            return self.__make_snapshot(SimulationEvent.REQUEST_GENERATED, nearest_generator.generator_id)
        elif len(self.__buffer) > 0:
            self.__global_time = nearest_device.available_at
            request = self.__buffer.get()
            request.left_buffer = self.__global_time
            nearest_device.handle(request)
            return self.__make_snapshot(SimulationEvent.REQUEST_HANDLED, nearest_device.device_id)
        else:
            self.__global_time = nearest_device.available_at
            nearest_device.pause()
            return self.__make_snapshot(SimulationEvent.DEVICE_PAUSED, nearest_device.device_id)
