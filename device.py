import logging


class Device:
    def __init__(self, device_id, tau, stats):
        self.__tau = tau
        self.__available_at = 0.0
        self.__current_request = None
        self.__device_id = device_id
        self.__stats = stats
        self.__paused = True

    def handle(self, request):
        logging.debug(f'{request.left_buffer} : {self.__device_id + 1} handles new request')
        self.__paused = False
        self.__stats.request_handled(self.__device_id, request)
        self.__current_request = request
        self.__available_at = request.left_buffer + self.__tau
        logging.debug(f'available at {self.__available_at}')

    def pause(self):
        logging.debug(f'{self.__available_at} : {self.__device_id} paused')
        self.__paused = True

    @property
    def available_at(self):
        return self.__available_at

    @property
    def current_request(self):
        return self.__current_request

    @property
    def paused(self):
        return self.__paused

    @property
    def device_id(self):
        return self.__device_id
