import logging


class Buffer:
    def __init__(self, capacity, stats):
        self.__capacity = capacity
        self.__buffer = [None] * capacity
        self.__cursor = 0
        self.__current_package = 0
        self.__stats = stats

    def __inc_cursor(self):
        self.__cursor = self.__cursor + 1
        if self.__cursor == self.__capacity:
            self.__cursor = 0

    def __len__(self):
        return self.size

    def __str__(self):
        return ' '.join(map(lambda item: str(item.source) if item is not None else '_', self.__buffer)) \
               + f' | active package: {self.__current_package}'

    def __chose_active_package(self, force=False):
        curr_package_size = sum(1 for item in self.__buffer if item is not None
                                and item.source == self.__current_package)
        if curr_package_size == 0 or force:
            self.__current_package = min(
                map(lambda item: item.source, filter(lambda x: x is not None, self.__buffer)), default=0
            )

    @property
    def size(self):
        return sum([1 for item in self.__buffer if item is not None])

    def insert(self, item):
        old_cursor = self.__cursor
        while self.__buffer[self.__cursor] is not None:
            self.__inc_cursor()
            if self.__cursor == old_cursor:
                break
        if self.__buffer[self.__cursor] is not None:
            self.__stats.request_rejected(self.__buffer[self.__cursor])
        self.__buffer[self.__cursor] = item
        self.__inc_cursor()
        self.__chose_active_package(force=True)

    def get(self):
        if self.size == 0:
            return None
        for i in range(self.__capacity):
            item = self.__buffer[i]
            if item is not None and item.source == self.__current_package:
                self.__buffer[i] = None
                self.__chose_active_package()
                return item
