# main.py
from argument import argument
from alerts import alert
from output import output
from collection import collection
import time
import json
CONFIG_FILE = "config.json"

def main():
    """
    Entry point of the System Monitor program.
    """
    args = argument()

    # Save thresholds (to config.json)
    save_thresholds(args.warning, args.danger)

    if args.daemon:
        run_daemon_mode(args, args.warning, args.danger, args.interval)
    else:
        run_default_mode(args, args.warning, args.danger)


def run_default_mode(args, warning, danger):
    data = collection()
    output(args, data)
    alert(data, warning, danger)

    
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
            run_default_mode(args, warning, danger)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nDaemon mode exited.")
        print("Thank you for using System Monitor. Goodbye!")


def save_thresholds(warning, danger):
    """
    Write the threshold into the Json file.
    """
    data = {"warning": warning, "danger": danger}
    with open(CONFIG_FILE, "w") as file:
        json.dump(data, file, indent=4)


if __name__ == "__main__":
    main()
    