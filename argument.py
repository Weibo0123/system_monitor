#argument.py
"""
This is the file that getting the comment-line arguments and manage the configuration.
Only the get_argument and save_thresholds will becalled outside the file
"""
import json
import argparse
CONFIG_FILE = "config.json"

def get_argument():
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
    if not 0 < value <= 100:
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