import time
import psutil

def get_cpu_usage(per_core=False):
    """
    Get the percentage of the CPU usage.
    """
    return psutil.cpu_percent(interval=0.1, percpu=per_core)


def get_memory_usage():
    """
    Get the percentage of the memory usage.
    """
    return psutil.virtual_memory()


def get_disk_usage():
    """
    Get the disk usage.
    """
    return psutil.disk_usage("/")


def get_net_speed(interval=1):
    """
    Get network speed.
    """
    old_value = psutil.net_io_counters()
    time.sleep(interval)
    new_value = psutil.net_io_counters()

    bytes_sent = (new_value.bytes_sent - old_value.bytes_sent) / interval
    bytes_recv = (new_value.bytes_recv - old_value.bytes_recv) / interval
    packets_sent = (new_value.packets_sent - old_value.packets_sent) / interval
    packets_recv = (new_value.packets_recv - old_value.packets_recv) / interval

    return [bytes_sent, bytes_recv, packets_sent, packets_recv]