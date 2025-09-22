# main.py
from argument import get_argument, save_thresholds
from alerts import check_and_warn
from output import print_output
from collection import collect_system_data
import time
CONFIG_FILE = "config.json"

def main():
    """
    Entry point of the System Monitor program.
    Parses commend line arguments and saves thresholds.
    And then run the mode based on user inputs.
    """
    args = get_argument()

    # Save thresholds (to config.json)
    save_thresholds(args.warning, args.danger)

    if args.daemon:
        run_daemon_mode(args, args.warning, args.danger, args.interval)
    else:
        run_default_mode(args, args.warning, args.danger)


def run_default_mode(args, warning, danger):
    """
    Collect system data once, print output, and chekc for alerts.
    """
    system_data = collect_system_data()
    print_output(args, system_data)
    check_and_warn(system_data, warning, danger)

    
def run_daemon_mode(args, warning, danger, interval=30):
    """
    Run the system monitor repeatly at a fixed interval (default 30 seconds).
    Allows user to stop with Ctrl + C.
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





if __name__ == "__main__":
    main()
    