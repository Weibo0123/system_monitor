import csv
import datetime
import os

LOG_FILE = "system_log.csv"

def log_system_data(data):
    exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a",  newline="") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp", "cpu", "mem", "disk", "net_up", "net_down"])
        writer.writerow([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data["cpu"],
            data["mem"].percent,
            data["disk"].percent,
            data["net"][0],
            data["net"][1]
        ])