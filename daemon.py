from logic import collect_args_and_print
import time

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
