import psutil
import argparse

def main():
    parser = argparse.ArgumentParser(description="The system monitor")
    parser.add_argument("-c", "--cpu", action="store_true", help="check the CPU")
    parser.add_argument("-m", "--mem", action="store_true", help="check the Memory")

    args = parser.parse_args()

    args_dict = vars(args)

    cpu_usage = get_cpu_usage()
    mem_usage = get_memory_usage()


    if not any(args_dict.values()):
        print(f"CPU Usage: {cpu_usage}%" )
        print(f"Memory Usage: {mem_usage.percent}%")
    else:
        if args.cpu:
            print(f"CPU Usage: {cpu_usage}%" )
        if args.mem:
            print(f"Memory Usage:")
            print(f"Total: {mem_usage.total / (1024 ** 3):.2f} GB")
            print(f"Used: {mem_usage.used / (1024 ** 3):.2f} GB")
            print(f"Available: {mem_usage.available/ (1024 ** 3):.2f} GB")
            print(f"Usage: {mem_usage.percent}%")

    


def get_cpu_usage():
    usage = psutil.cpu_percent(interval=0.1)
    return usage

def get_memory_usage():
    usage = psutil.virtual_memory()
    return usage

if __name__ == "__main__":
    main()