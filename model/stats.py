class Stats:
    def __init__(self, num_sources, num_devices):
        self.__requests_handled_by_source = [0] * num_sources
        self.__requests_handled_by_device = [0] * num_devices
        self.__request_rejected = [0] * num_sources
        self.__total_wait_time = 0.0
        self.__time_paused = [0] * num_devices
        self.__simulation_time = 0

    def request_rejected(self, request):
        self.__request_rejected[request.source] += 1

    def request_handled(self, device_id, request):
        self.__requests_handled_by_device[device_id] += 1
        self.__requests_handled_by_source[request.source] += 1
        self.__total_wait_time += (request.left_buffer - request.created)

    def device_continued(self, device_id, pause_duration):
        self.__time_paused[device_id] += pause_duration

    def  simulation_ended(self, global_time):
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
        self_str += f'Average wait time: {self.__total_wait_time / sum(self.__requests_handled_by_source)}'
        return self_str

    @property
    def total_handled(self):
        return sum(self.__requests_handled_by_source)

    @property
    def total_rejected(self):
        return sum(self.__request_rejected)

    @property
    def rejection_probability(self):
        return self.total_rejected / (self.total_rejected + self.total_handled)

    @property
    def pause_ratio(self):
        if self.__simulation_time == 0:
            return -1
        return sum(self.__time_paused) / (self.__simulation_time * len(self.__time_paused))

    @property
    def average_wait_time(self):
        return self.__total_wait_time / sum(self.__requests_handled_by_source)
