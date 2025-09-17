#logic.py
from collection import get_cpu_usage, get_memory_usage, get_disk_usage, get_net_speed
from print import print_all_usage_percentage, print_cpu_usage, print_memory_usage, print_disk_usage, print_net_speed
from alerts import check_and_warning

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
    