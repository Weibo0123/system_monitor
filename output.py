#print.py
def output(args, data):
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

