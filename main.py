import psutil
import argparse

def main():
    parser = argparse.ArgumentParser(description="The system monitor")
    parser.add_argument("-c", "--cpu", action="store_true", help="check the CPU")
    parser.add_argument("-m", "--mem", action="store_true", help="check the Memory")
    parser.add_argument("-d", "--disk", action="store_true", help="check the Disk")

    args = parser.parse_args()

    args_dict = vars(args)

    cpu_usage = get_cpu_usage()
    mem_usage = get_memory_usage()
    disk_usage = get_disk_usage()


    if not any(args_dict.values()):
        print_all_usage_percentage(cpu_usage, mem_usage, disk_usage)
    else:
        if args.cpu:
            print_cpu_usage(cpu_usage)
        if args.mem:
            print_memory_usage(mem_usage)
        if args.disk:
            print_disk_usage(disk_usage)

        


def get_cpu_usage():
    usage = psutil.cpu_percent(interval=0.1)
    return usage

def get_memory_usage():
    usage = psutil.virtual_memory()
    return usage

def get_disk_usage():
    usage = psutil.disk_usage("/")
    return usage

def print_all_usage_percentage(cpu, mem, disk):
        print(f"CPU Usage: {cpu}%" )
        print(f"Memory Usage: {mem.percent}%")
        print(f"Disk Usage: {disk.percent}%")

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

if __name__ == "__main__":
    main()