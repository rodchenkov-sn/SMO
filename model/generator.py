from model.request import Request

import math
import random
import logging


class Generator:
    def __init__(self, generator_id, lmb, stats):
        self.__id = generator_id
        self.__lmb = lmb
        self.__generated = 0
        self.__new_request_time = 0.0
        self.__stats = stats

    def generate(self):
        logging.debug(f'{self.__new_request_time} : {self.__id + 1} generates new request')
        request = Request(self.__new_request_time, self.__id)
        self.__new_request_time += -1 / self.__lmb * math.log(random.uniform(0, 1), math.e)
        self.__generated += 1
        logging.debug(f'new request at {self.__new_request_time}')
        return request

    @property
    def new_request_time(self):
        return self.__new_request_time

    @property
    def generated(self):
        return self.__generated

    @property
    def generator_id(self):
        return self.__id
