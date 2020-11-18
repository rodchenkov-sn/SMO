from device import Device
from buffer import Buffer
from generator import Generator
from stats import Stats


def main():
    try:
        stats = Stats()
        max_requests = 100
        devices = [Device(x, 1, stats) for x in range(3)]
        generators = [Generator(x, 1, stats) for x in range(3)]
        buffer = Buffer(10, stats)
        while stats.total_handled < max_requests:
            nearest_generator = min(generators, key=lambda generator: generator.new_request_time)
            nearest_device = min(devices, key=lambda device: device.available_at)
            if nearest_device.available_at < nearest_generator.new_request_time and buffer.size > 0:
                print(f'! device {nearest_device.device_id} handles new request at ', end='')
                global_time = nearest_device.available_at
                handled_request = buffer.get()
                handled_request.left_buffer = global_time
                nearest_device.handle(handled_request)
            elif nearest_generator.new_request_time <= nearest_device.available_at:
                print(f'! generator {nearest_generator.generator_id} generates new request at ', end='')
                global_time = nearest_generator.new_request_time
                new_request = nearest_generator.generate()
                buffer.insert(new_request)
            else:
                nearest_device.pause_until(nearest_generator.new_request_time)
                continue
            print(global_time)
            print(f'  buffer: {str(buffer)}')
            print(f'  request handled: {stats.total_handled}')
            print(f'  request rejected: {stats.total_rejected}')
            print(f'  devices: {" ".join(map(lambda device: "Waiting" if device.paused else "Working", devices))}')
        print('\n====================================\n')
        stats.show_stats()
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
