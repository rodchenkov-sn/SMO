class Request:
    def __init__(self, created, source):
        self.created = created
        self.source = source
        self.left_buffer = None

    def __str__(self):
        return f'(source: {self.source}; created: {self.created}; left_buffer: {self.left_buffer})'
