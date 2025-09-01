import psutil

def main():
    cpu_usage = get_cpu_usage()
    mem_usage = get_memory_usage()
    print(f"CPU Usage: {cpu_usage}%" )
    print(f"Memory Usage: {mem_usage}%")



def get_cpu_usage():
    usage = psutil.cpu_percent(interval=1)
    return usage

def get_memory_usage():
    usage = psutil.virtual_memory()
    return usage.percent

if __name__ == "__main__":
    main()