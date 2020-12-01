class Stats:
    def __init__(self):
        self.__requests_handled_by_source = [0, 0, 0]
        self.__requests_handled_by_device = [0, 0, 0]
        self.__request_rejected = [0, 0, 0]
        self.__total_wait_time = 0.0

    def request_rejected(self, request):
        self.__request_rejected[request.source] += 1

    def request_handled(self, device_id, request):
        self.__requests_handled_by_device[device_id] += 1
        self.__requests_handled_by_source[request.source] += 1
        self.__total_wait_time += (request.left_buffer - request.created)

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
