#log.py
import csv
import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "system_log.csv")

def log_system_data(data):
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    exists = os.path.exists(LOG_FILE)

    cpu = data.get("cpu")
    memory = getattr(data.get("memory"), "percent", None)
    disk = getattr(data.get("disk"), "percent", None)
    net_speed = data.get("net_speed") or [None, None, None, None]

    with open(LOG_FILE, "a",  newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["timestamp", "cpu", "mem", "disk", "net_up", "net_down"])
        writer.writerow([
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cpu,
            memory,
            disk,
            net_speed[0],
            net_speed[1],
        ])