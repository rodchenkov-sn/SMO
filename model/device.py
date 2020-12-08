from model.stats import Stats
from enum import Enum, auto

import logging


class DeviceState(Enum):
    WORKING = auto()
    PAUSED = auto()


class Device:
    def __init__(self, device_id: int, tau: float, stats: Stats):
        self.__tau = tau
        self.__available_at = 0.0
        self.__current_request = None
        self.__device_id = device_id
        self.__stats = stats
        self.__state = DeviceState.PAUSED
        self.__time_paused = 0.0

    def handle(self, request):
        logging.debug(f'{request.left_buffer} : {self.__device_id + 1} handles new request')
        if self.__state is DeviceState.PAUSED:
            self.__state = DeviceState.WORKING
            self.__stats.device_continued(self.__device_id, request.left_buffer - self.__time_paused)
        self.__stats.request_handled(self.__device_id, request, self.__tau)
        self.__current_request = request
        self.__available_at = request.left_buffer + self.__tau
        logging.debug(f'available at {self.__available_at}')

    def pause(self):
        logging.debug(f'{self.__available_at} : {self.__device_id} paused')
        self.__state = DeviceState.PAUSED
        self.__time_paused = self.__available_at
        self.__current_request = None

    @property
    def available_at(self):
        return self.__available_at

    @property
    def current_request(self):
        return self.__current_request

    @property
    def paused(self):
        return self.__state is DeviceState.PAUSED

    @property
    def state(self):
        return self.__state

    @property
    def device_id(self):
        return self.__device_id

    @property
    def current_request_source(self):
        return self.__current_request.source if self.__current_request is not None else None
