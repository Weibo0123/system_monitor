import psutil
import argparse
import time

def main():
    parser = argparse.ArgumentParser(description="The system monitor")
    parser.add_argument("-c", "--cpu", action="store_true", help="check the CPU")
    parser.add_argument("-m", "--mem", action="store_true", help="check the Memory")
    parser.add_argument("-d", "--disk", action="store_true", help="check the Disk")
    parser.add_argument("-n", "--net", action="store_true", help="check the Network")
    parser.add_argument("-a", "--daemon", action="store_true", help="run in daemon mode(every 30s)")


    args = parser.parse_args()

    if args.daemon:
        print("Daemon mode enabled")
        time.sleep(1)
        print("Collecting system information every 30 seconds.")
        time.sleep(1)
        print("Press Ctrl + C to exit\nf")
        try:
            while True:
                collect_args_and_print(args)
                time.sleep(30)
        except KeyboardInterrupt:
            print("\n\n Daemon mode exited.")
            print("Thank you for using System Monitor. Goodbye!")
    else:
        collect_args_and_print(args)
        


def get_cpu_usage():
    usage = psutil.cpu_percent(interval=0.1)
    return usage


def get_each_core_of_cpu_usage():
    usage = psutil.cpu_percent(interval=0.1, percpu=True)
    return usage


def get_memory_usage():
    usage = psutil.virtual_memory()
    return usage


def get_disk_usage():
    usage = psutil.disk_usage("/")
    return usage


def get_net_speed(interval=1):
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
    print(f"Download Speed: {net[1] / (1024 ** 2):.2f} MB\n")


def print_cpu_usage(usage, cores):
    print(f"CPU Usage: {usage}%")
    for i, usage in enumerate(cores):
        print(f"CPU Core {i+1}: {usage}%\n")


def print_memory_usage(mem):
    print(f"Memory Usage:")
    print(f"Total: {mem.total / (1024 ** 3):.2f} GB")
    print(f"Used: {mem.used / (1024 ** 3):.2f} GB")
    print(f"Available: {mem.available/ (1024 ** 3):.2f} GB")
    print(f"Usage: {mem.percent}%\n")


def print_disk_usage(disk):
    print(f"Disk Usage:")
    print(f"Total: {disk.total / (1024 ** 3):.2f} GB")
    print(f"Used: {disk.used / (1024 ** 3):.2f} GB")
    print(f"Free: {disk.free/ (1024 ** 3):.2f} GB")
    print(f"Usage: {disk.percent}%\n")


def print_net_speed(net):
    print(f"Network Speed:")
    print(f"Upload Speed: {net[0] / (1024):.2f} KB/s")
    print(f"Download Speed: {net[1] / (1024):.2f} KB/s")
    print(f"Packets Upload: {int(net[2])} Packets/s")
    print(f"Packets Download: {int(net[3])} Packets/s\n")


def collect_args_and_print(args):
    args_dict = vars(args).copy()
    args_dict.pop("daemon", None)

    cpu_usage = get_cpu_usage()
    each_core_of_cpu_usage = get_each_core_of_cpu_usage()
    mem_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    net_speed = get_net_speed()
    if not any(args_dict.values()):
        print_all_usage_percentage(cpu_usage, mem_usage, disk_usage, net_speed)
    else:
        if args.cpu:
            print_cpu_usage(cpu_usage, each_core_of_cpu_usage)
        if args.mem:
            print_memory_usage(mem_usage)
        if args.disk:
            print_disk_usage(disk_usage)
        if args.net:
            print_net_speed(net_speed)
    
    check_and_warning(cpu_usage, mem_usage, disk_usage)
    

def check_and_warning(cpu, mem, disk):
    warning_thresholds, danger_thresholds = get_thresholds()
    get_warning(cpu, mem, disk, warning_thresholds, danger_thresholds)


def get_thresholds(warning_thresholds=None, danger_thresholds=None):
    if not warning_thresholds:
        warning_thresholds = 70
    if not danger_thresholds:
        danger_thresholds = 90 
    return warning_thresholds, danger_thresholds


def get_warning(cpu, mem, disk, warning_thresholds, danger_thresholds):
    if cpu > danger_thresholds:
        print_danger(f"[DANGER] Danger CPU Usage Detected: {cpu}%")
    elif cpu > warning_thresholds:
        print_warning(f"[WARNING] High CPU Usage Detected: {cpu}%")

    if mem.percent > danger_thresholds:
        print_danger(f"[DANGER] Danger Memory Usage Detected: {mem.percent}%")
    elif mem.percent > warning_thresholds:
        print_warning(f"[WARNING] High Memory Usage Detected: {mem.percent}%")

    if disk.percent > danger_thresholds:
        print_danger(f"[DANGER] Danger Disk Usage Detected: {disk.percent}%")
    elif disk.percent > warning_thresholds:
        print_warning(f"[WARNING] High Disk Usage Detected: {disk.percent}%")


def print_warning(str):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}{str}{RESET}")

def print_danger(str):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}{str}{RESET}")
    
    



if __name__ == "__main__":
    main()