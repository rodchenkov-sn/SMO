from typing import List


class Stats:
    def __init__(self, num_sources, num_devices):
        self.__requests_handled_by_source = [0] * num_sources
        self.__requests_handled_by_device = [0] * num_devices
        self.__request_rejected = [0] * num_sources
        self.__handle_time = [0] * num_sources
        self.__total_wait_time = [0.0] * num_sources
        self.__time_paused = [0.0] * num_devices
        self.__simulation_time = 0

    def request_rejected(self, request):
        self.__request_rejected[request.source] += 1

    def request_handled(self, device_id, request, handle_time):
        self.__requests_handled_by_device[device_id] += 1
        self.__requests_handled_by_source[request.source] += 1
        self.__total_wait_time[request.source] += (request.left_buffer - request.created)
        self.__handle_time[request.source] += handle_time

    def device_continued(self, device_id, pause_duration):
        self.__time_paused[device_id] += pause_duration

    def set_current_time(self, global_time):
        self.__simulation_time = global_time

    def __str__(self):
        self_str = ''
        self_str += 'Requests handled (grouped by device_id)\n'
        for i in range(3):
            self_str += f'\t{i + 1}: {self.__requests_handled_by_device[i]}\n'
        self_str += 'Requests handled (grouped by source_id)\n'
        for i in range(3):
            self_str += f'\t{i + 1}: {self.__requests_handled_by_source[i]}\n'
        self_str += 'Requests rejected\n'
        for i in range(3):
            self_str += f'\t{i + 1}: {self.__request_rejected[i]}\n'
        self_str += f'Average wait time: {sum(self.__total_wait_time) / sum(self.__requests_handled_by_source)}'
        return self_str

    @property
    def average_handle_time(self) -> float:
        return sum(self.__handle_time) / self.total_handled

    @property
    def average_handle_time_by_source(self) -> List[float]:
        return [t / h for t, h in zip(self.__handle_time, self.total_handled_by_source)]

    @property
    def total_handled(self) -> int:
        return sum(self.total_handled_by_source)

    @property
    def total_handled_by_source(self) -> List[int]:
        return self.__requests_handled_by_source

    @property
    def total_rejected(self) -> int:
        return sum(self.total_rejected_by_source)

    @property
    def total_rejected_by_source(self) -> List[int]:
        return self.__request_rejected

    @property
    def total_generated(self) -> int:
        return sum(self.total_generated_by_source)

    @property
    def total_generated_by_source(self) -> List[int]:
        return [h + r for h, r in zip(self.__request_rejected, self.__requests_handled_by_source)]

    @property
    def rejection_probability(self) -> float:
        return self.__request_rejected / self.total_generated

    @property
    def rejection_probability_by_source(self) -> List[float]:
        return [t / r for t, r in zip(self.__request_rejected, self.total_generated_by_source)]

    @property
    def pause_ratio(self) -> float:
        return sum(self.__time_paused) / (self.__simulation_time * len(self.__time_paused))

    @property
    def pause_ratio_by_device(self) -> List[float]:
        return list(map(lambda p: p / self.__simulation_time, self.__time_paused))

    @property
    def average_wait_time(self) -> float:
        return sum(self.__total_wait_time) / self.total_handled

    @property
    def average_wait_time_by_source(self) -> List[float]:
        return [w / t for w, t in zip(self.__total_wait_time, self.__requests_handled_by_source)]
