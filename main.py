import psutil

def main():
    cpu_usage = get_cpu_usage()
    print(f"CPU usage: {cpu_usage}%" )


def get_cpu_usage():
    usage = psutil.cpu_percent(interval=1)
    return usage

if __name__ == "__main__":
    main()