from device import Device
from buffer import Buffer
from generator import Generator
from stats import Stats

import logging
import sys


def main():
    try:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(message)s')
        stats = Stats()
        max_requests = 100
        devices = [Device(x, x + 1, stats) for x in range(3)]
        generators = [Generator(x, 1, stats) for x in range(3)]
        buffer = Buffer(3, stats)
        while stats.total_handled < max_requests:
            nearest_generator = min(generators, key=lambda generator: generator.new_request_time)
            nearest_device = min(
                filter(lambda device: not device.paused, devices),
                key=lambda device: device.available_at,
                default=None
            )
            if nearest_device is None or nearest_generator.new_request_time <= nearest_device.available_at:
                global_time = nearest_generator.new_request_time
                new_request = nearest_generator.generate()
                paused_devices = list(filter(lambda device: device.paused, devices))
                if len(paused_devices) > 0:
                    new_request.left_buffer = global_time
                    paused_devices[0].handle(new_request)
                else:
                    buffer.insert(new_request)
            elif len(buffer) > 0:
                global_time = nearest_device.available_at
                request = buffer.get()
                request.left_buffer = global_time
                nearest_device.handle(request)
            else:
                nearest_device.pause()
            logging.debug(f'buffer : {buffer}')
            logging.debug(f'handled : {stats.total_handled}')
            logging.debug(f'rejected : {stats.total_rejected}')
            logging.debug(f'devices : {" ".join(map(lambda device: "P" if device.paused else "W", devices))}\n')
        logging.info('====================================\n')
        logging.info(stats)
    except Exception as ex:
        logging.critical(f'\nAn error occurred while simulating SMO: {gex}')


if __name__ == '__main__':
    main()
