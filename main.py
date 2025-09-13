"""
System Monitor

Description:
    This code helps you to monitor your system, it could work on Linux, Windows and Mac.
    It can help you check CPU, Memory, Disk and Network
    It support daemon mode
    There is also warning and danger alerts
"""

import argparse
import time
import json
import psutil

CONFIG_FILE = "config.json"
# region Main
# Main Function
def main():
    """
    The main loop of the program.
    """
    args = parse_args()
    save_thresholds(args.warning, args.danger)

    if args.daemon:
        run_daemon_mode(args, args.warning, args.danger, args.interval)
    else:
        collect_args_and_print(args, args.warning, args.danger)
#endregion



# region Argument
# Argument Handling
def parse_args():
    """
    Get the argument by the command from users.
    """
    default_thresholds = load_thresholds()

    parser = argparse.ArgumentParser(description="The system monitor")
    parser.add_argument("-c", "--cpu", action="store_true", help="check the CPU")
    parser.add_argument("-m", "--mem", action="store_true", help="check the Memory")
    parser.add_argument("-d", "--disk", action="store_true", help="check the Disk")
    parser.add_argument("-n", "--net", action="store_true", help="check the Network")
    parser.add_argument("-a", "--daemon", action="store_true", help="run in daemon mode(every 30s)")
    parser.add_argument("--warning", type=get_int_between_0_and_100, default=default_thresholds["warning"], help=f"Warning threshold (default: {default_thresholds['warning']})")
    parser.add_argument("--danger", type=get_int_between_0_and_100, default=default_thresholds["danger"], help=f"Danger threshold (default: {default_thresholds['danger']})")
    parser.add_argument("--interval", type=get_positive_int, default=30, help="interval in seconds for daemon mode(default: 30s)")
    return parser.parse_args()


def get_int_between_0_and_100(value):
    """
    Get the correct number for the thresholds for the warning and danger.
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("The threshold must be a positive integer between 0 to 100")
    if not 0 < value < 100:
        raise argparse.ArgumentTypeError("The threshold must be a positive integer between 0 to 100")
    return value


def get_positive_int(value):
    """
    Get the correct number for the thresholds for interval in the daemon mode
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("The interval must be a positive integer")
    if not value > 0:
        raise argparse.ArgumentTypeError("The interval must be a positive integer")
    return value
    

def save_thresholds(warning, danger):
    """
    Write the threshold into the Json file.
    """
    data = {"warning": warning, "danger": danger}
    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_thresholds():
    """
    Get the threshold from the file.
    """
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {"warning": 70, "danger": 90}
#endregion



# region Collection
# System Data Collection
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
#endregion



# region Print
# Printing Functions
def print_all_usage_percentage(cpu, mem, disk, net):
    """
    Print percentage of all the parts the function check.
    """
    print(f"CPU Usage: {cpu}%" )
    print(f"Memory Usage: {mem.percent}%")
    print(f"Disk Usage: {disk.percent}%")
    print(f"Download Speed: {net[1] / 1024:.2f} KB\n")

def print_section(title, data):
    """
    Print a title and a dictionary.
    """
    print(f"{title}:")
    for key, value in data.items():
        print(f"{key}: {value}")
    print()


def print_cpu_usage(usage, cores):
    """
    Return a dictionary of the CPU usage.
    """
    data = {"Total": f"{usage}%"}
    for i, core in enumerate(cores):
        data[f"Core {i+1}"] = f"{core}%"
    print_section("CPU Usage", data)


def print_memory_usage(mem):
    """
    Return a dictionary of the memory usage.
    """
    print_section("Memory Usage", 
    {
        "Total": f"{mem.total / (1024 ** 3):.2f} GB",
        "Used": f"{mem.used / (1024 ** 3):.2f} GB",
        "Available": f"{mem.available / (1024 ** 3):.2f} GB",
        "Usage": f"{mem.percent}%"
    })


def print_disk_usage(disk):
    """
    Return a dictionary of the disk usage.
    """
    print_section("Disk Usage",
    {
        "Total": f"{disk.total / (1024 ** 3):.2f} GB",
        "Used": f"{disk.used / (1024 ** 3):.2f} GB",
        "Free": f"{disk.free / (1024 ** 3):.2f} GB",
        "Usage": f"{disk.percent}%"
    })


def print_net_speed(net):
    """
    Return a dictionary of the network speed.
    """
    print_section("Network Speed", 
    {
        "Upload Speed": f"{net[0] / 1024:.2f} KB/s",
        "Download Speed": f"{net[1] / 1024:.2f} KB/s",
        "Packets Upload": f"{int(net[2])} Packets/s",
        "Packets Download": f"{int(net[3])} Packets/s"
    })
# endregion



# region Alerts
# Danger / Warning Alerts
def get_alerts(data, warning, danger):
    """
    Return a dictionary of the things that should warn the user.
    """
    alerts = []

    if data["cpu"] >= danger:
        alerts.append(("danger", f"Danger CPU Usage Detected: {data['cpu']}%"))
    elif data["cpu"] >= warning:
        alerts.append(("warning", f"High CPU Usage Detected: {data['cpu']}%"))

    if data["mem"].percent >= danger:
        alerts.append(("danger", f"Danger Memory Usage Detected: {data['mem'].percent}%"))
    elif data["mem"].percent >= warning:
        alerts.append(("warning", f"High Memory Usage Detected: {data['mem'].percent}%"))

    if data["disk"].percent >= danger:
        alerts.append(("danger", f"Danger Disk Usage Detected: {data['disk'].percent}%"))
    elif data["disk"].percent >= warning:
        alerts.append(("warning", f"High Disk Usage Detected: {data['disk'].percent}%"))

    return alerts


def check_and_warning(data, warning, danger):
    """
    Get the alerts and print them.
    """
    alerts = get_alerts(data, warning, danger)
    print_alerts(alerts)


def print_alerts(alerts):
    """
    Print the alerts.
    """
    for level, msg in alerts:
        add_color_to_alerts(level, msg)


def add_color_to_alerts(level, msg):
    """
    Add color to the alerts.
    """
    colors = {"warning": "\033[93m", "danger": "\033[91m"}
    RESET = "\033[0m"
    prefixes = {"warning": "[WARNING]", "danger": "[DANGER]"}
    print(f"{colors[level]}{prefixes[level]} {msg}{RESET}")  
# endriegion



# region Logic
# Logic Functions

    
def collect_system_data():
    """
    Collect the system data includes the cpu, each cores of cpu, memory, disk, network.
    """
    return{
        "cpu": get_cpu_usage(),
        "cpu_cores": get_cpu_usage(per_core=True),
        "mem": get_memory_usage(),
        "disk": get_disk_usage(),
        "net": get_net_speed()
    }


def print_select_data(args, data):
    """
    Print the data that user asks.
    """
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
    """
    collect the data that user asks and print them out.
    It also checks if there are anything that needs to warn the user
    """
    data = collect_system_data()
    print_select_data(args, data)
    check_and_warning(data, warning, danger)


def run_daemon_mode(args, warning, danger, interval=30):
    """
    run the daemon mode, if the function doesn't get an interval.
    The interval will be 30 seconds by default.
    """
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
        print("\n\nDaemon mode exited.")
        print("Thank you for using System Monitor. Goodbye!")
#endregion

    

if __name__ == "__main__":
    main()