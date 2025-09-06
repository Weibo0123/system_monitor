import argparse
import time
import psutil
import sys

def main():
    parser = argparse.ArgumentParser(description="The system monitor")
    parser.add_argument("-c", "--cpu", action="store_true", help="check the CPU")
    parser.add_argument("-m", "--mem", action="store_true", help="check the Memory")
    parser.add_argument("-d", "--disk", action="store_true", help="check the Disk")
    parser.add_argument("-n", "--net", action="store_true", help="check the Network")
    parser.add_argument("-a", "--daemon", action="store_true", help="run in daemon mode(every 30s)")
    parser.add_argument("--warning", type=get_positive_int, default=70, help="Warning threshold (default: 70)")
    parser.add_argument("--danger", type=get_positive_int, default=90, help="Danger threshold (default: 90)")

    args = parser.parse_args()

    warning, danger = args.warning, args.danger



    if args.daemon:
        run_daemon_mode(args, warning, danger)
    else:
        collect_args_and_print(args, warning, danger)
        

def run_daemon_mode(args, warning, danger, interval=30):
    print("Daemon mode enabled")
    time.sleep(1)
    print(f"Collecting system information every {interval} seconds.")
    time.sleep(1)
    print("Press Ctrl + C to exit\n")
    try:
        while True:
            collect_args_and_print(args, warning, danger)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\n Daemon mode exited.")
        print("Thank you for using System Monitor. Goodbye!")


def get_cpu_usage():
    usage = psutil.cpu_percent(interval=0.1)
    return usage


def get_cpu_usage_per_core():
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


def collect_system_data():
    return{
        "cpu": get_cpu_usage(),
        "cpu_cores": get_cpu_usage_per_core(),
        "mem": get_memory_usage(),
        "disk": get_disk_usage(),
        "net": get_net_speed()
    }

def print_select_data(args, data):
    if not(args.cpu or args.mem or args.disk or args.net):
        print_all_usage_percentage(data["cpu"], data["mem"], data["disk"], data["net"])
    else:
        if args.cpu:
            print_cpu_usage(data["cpu"], data["cpu_cores"])
        if args.mem:
            print_memory_usage(data["mem"])
        if args.disk:
            print_disk_usage(data["disk"])
        if args.net:
            print_net_speed(data["net"])


def collect_args_and_print(args, warning, danger):
    data = collect_system_data()
    print_select_data(args, data)
    check_and_warning(data, warning, danger)


def check_and_warning(data, warning, danger):
    get_warning(data["cpu"], data["mem"], data["disk"], warning, danger)

def get_warning(cpu, mem, disk, warning, danger):
    if cpu > danger:
        print_danger(f"CPU Usage Detected: {cpu}%")
    elif cpu > warning:
        print_warning(f"CPU Usage Detected: {cpu}%")

    if mem.percent > danger:
        print_danger(f"Memory Usage Detected: {mem.percent}%")
    elif mem.percent > warning:
        print_warning(f"Memory Usage Detected: {mem.percent}%")

    if disk.percent > danger:
        print_danger(f"Disk Usage Detected: {disk.percent}%")
    elif disk.percent > warning:
        print_warning(f"Disk Usage Detected: {disk.percent}%")


def print_warning(s):
    YELLOW = "\033[93m"
    RESET = "\033[0m"
    print(f"{YELLOW}[WARNING] High {s}{RESET}")

def print_danger(s):
    RED = "\033[91m"
    RESET = "\033[0m"
    print(f"{RED}[DANGER] Danger {s}{RESET}")

def get_positive_int(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("The threshold must be a positive integer")
    if value < 0:
        raise argparse.ArgumentTypeError("The threshold must be a positive integer")
    return value
    
if __name__ == "__main__":
    main()