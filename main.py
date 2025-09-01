import psutil
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description="The system monitor")
    parser.add_argument("-c", "--cpu", action="store_true", help="check the CPU")
    parser.add_argument("-m", "--mem", action="store_true", help="check the Memory")
    parser.add_argument("-d", "--disk", action="store_true", help="check the Disk")
    parser.add_argument("-n", "--net", action="store_true", help="check the Network")

    args = parser.parse_args()

    args_dict = vars(args)

    cpu_usage = get_cpu_usage()
    mem_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    net_speed = get_net_speed()

    


    if not any(args_dict.values()):
        print_all_usage_percentage(cpu_usage, mem_usage, disk_usage, net_speed)
    else:
        if args.cpu:
            print_cpu_usage(cpu_usage)
        if args.mem:
            print_memory_usage(mem_usage)
        if args.disk:
            print_disk_usage(disk_usage)
        if args.net:
            print_net_speed(net_speed)
        


def get_cpu_usage():
    usage = psutil.cpu_percent(interval=0.1)
    return usage

def get_memory_usage():
    usage = psutil.virtual_memory()
    return usage

def get_disk_usage():
    usage = psutil.disk_usage("/")
    return usage

def get_net_speed(interval=0.1):
    old_value = psutil.net_io_counters()
    time.sleep(interval)
    new_value = psutil.net_io_counters()

    bytes_sent = (new_value.bytes_sent - old_value.bytes_sent) / interval
    bytes_recv = (new_value.bytes_recv - old_value.bytes_recv) / interval
    packets_sent = (new_value.packets_sent - old_value.packets_sent) / interval
    packets_recv = (new_value.packets_recv - old_value.packets_recv) / interval

    return [bytes_sent, bytes_recv, packets_sent, packets_recv]


def print_all_usage_percentage(cpu, mem, disk, net):
        print(f"CPU Usage: {cpu}%" )
        print(f"Memory Usage: {mem.percent}%")
        print(f"Disk Usage: {disk.percent}%")
        print(f"Network Speed: {net[1] / (1024 ** 2):.2f} MB")

def print_cpu_usage(cpu):
    print(f"CPU Usage: {cpu}%" )

def print_memory_usage(mem):
    print(f"Memory Usage:")
    print(f"Total: {mem.total / (1024 ** 3):.2f} GB")
    print(f"Used: {mem.used / (1024 ** 3):.2f} GB")
    print(f"Available: {mem.available/ (1024 ** 3):.2f} GB")
    print(f"Usage: {mem.percent}%")

def print_disk_usage(disk):
    print(f"Disk Usage:")
    print(f"Total: {disk.total / (1024 ** 3):.2f} GB")
    print(f"Used: {disk.used / (1024 ** 3):.2f} GB")
    print(f"Free: {disk.free/ (1024 ** 3):.2f} GB")
    print(f"Usage: {disk.percent}%")

def print_net_speed(net):
    print(f"Network Speed:")
    print(f"Upload Speed: {net[0] / (1024 ** 2):.2f} MB")
    print(f"Download Speed: {net[1] / (1024 ** 2):.2f} MB")
    print(f"Packets Upload: {net[2] / (1024 ** 2):.2f} MB")
    print(f"Packets Download: {net[3] / (1024 ** 2):.2f} MB")



if __name__ == "__main__":
    main()