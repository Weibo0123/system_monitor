#alerts.py
"""
This is the file that check the warning and danger thresholds and print alerts.
Only the check_and_warn will be called outside this file.
"""
def check_and_warn(data, warning, danger):
    """
    Get the alerts and print them by calling get_alerts and print_alerts.
    This is function will be called in main.
    """
    alerts = get_alerts(data, warning, danger)
    print_alerts(alerts)


def get_alerts(data, warning, danger):
    """
    Check the system data and the thresholds.
    Return a dictionary of the things that should warn the user.
    """
    alerts = []

    if data["cpu"] >= danger:
        alerts.append(("danger", f"Danger CPU Usage Detected: {data['cpu']}%"))
    elif data["cpu"] >= warning:
        alerts.append(("warning", f"High CPU Usage Detected: {data['cpu']}%"))

    if data["mem"].percent >= danger:
        alerts.append(("danger", f"Danger Memory Usage Detected: {data['mem'].percent}%"))
    elif data["mem"].percent >= warning:
        alerts.append(("warning", f"High Memory Usage Detected: {data['mem'].percent}%"))

    if data["disk"].percent >= danger:
        alerts.append(("danger", f"Danger Disk Usage Detected: {data['disk'].percent}%"))
    elif data["disk"].percent >= warning:
        alerts.append(("warning", f"High Disk Usage Detected: {data['disk'].percent}%"))

    return alerts


def print_alerts(alerts):
    """
    Print the alerts that should show users in color.
    """
    colors = {"warning": "\033[93m", "danger": "\033[91m"}
    RESET = "\033[0m"
    prefixes = {"warning": "[WARNING]", "danger": "[DANGER]"}
    for level, msg in alerts:
        print(f"{colors[level]}{prefixes[level]} {msg}{RESET}")  

    