import pytest
import json
from main import get_positive_int, get_alerts, load_thresholds, save_thresholds
import argparse

def test_get_positive_int():
    assert get_positive_int(10) == 10
    assert get_positive_int(0) == 0
    assert get_positive_int(100) == 100
    assert get_positive_int("80") == 80
    assert get_positive_int("75") == 75
    with pytest.raises(argparse.ArgumentTypeError):
        get_positive_int("-5")
    with pytest.raises(argparse.ArgumentTypeError):
        get_positive_int("120")
    with pytest.raises(argparse.ArgumentTypeError):
        get_positive_int("cat")


class MockUsage:
    def __init__(self, percent):
        self.percent = percent


def test_get_alerts():
    data = {
        "cpu": 70,
        "mem": MockUsage(50),
        "disk": MockUsage(40)
    }
    alerts = get_alerts(data, warning=70, danger=90)
    assert alerts == [("warning", "High CPU Usage Detected: 70%")]

    data = {
        "cpu": 80,
        "mem": MockUsage(75),
        "disk": MockUsage(70)
    }
    alerts = get_alerts(data, warning=70, danger=90)
    assert ("warning", "High CPU Usage Detected: 80%") in alerts
    assert ("warning", "High Memory Usage Detected: 75%") in alerts
    assert ("warning", "High Disk Usage Detected: 70%") in alerts

    data = {
        "cpu": 90,
        "mem": MockUsage(70),
        "disk": MockUsage(20)
    }
    alerts = get_alerts(data, warning=70, danger=90)
    assert ("danger", "Danger CPU Usage Detected: 90%") in alerts
    assert ("warning", "High Memory Usage Detected: 70%") in alerts

    data = {
        "cpu": 50,
        "mem": MockUsage(70),
        "disk": MockUsage(90)
    }
    alerts = get_alerts(data, warning=50, danger=70)
    assert ("warning", "High CPU Usage Detected: 50%") in alerts
    assert ("danger", "Danger Memory Usage Detected: 70%") in alerts
    assert ("danger", "Danger Disk Usage Detected: 90%") in alerts

    data = {
        "cpu": 50,
        "mem": MockUsage(40),
        "disk": MockUsage(30)
    }
    alerts = get_alerts(data, warning=70, danger=90)
    assert alerts == []

    
def test_load_and_save_thresholds(tmp_path, monkeypatch):
    config_file = tmp_path / "config.json"
    monkeypatch.setattr("main.CONFIG_FILE", str(config_file))

    save_thresholds(50, 70)
    with open(config_file) as file:
        data = json.load(file)
    assert data == {"warning": 50, "danger": 70}
    data = load_thresholds()
    assert data == {"warning": 50, "danger": 70}

    save_thresholds(0, 0)
    with open(config_file) as file:
        data = json.load(file)
    assert data == {"warning": 0, "danger": 0}
    data = load_thresholds()
    assert data == {"warning": 0, "danger": 0}

    save_thresholds(100, 100)
    with open(config_file) as file:
        data = json.load(file)
    assert data == {"warning": 100, "danger": 100}
    data = load_thresholds()
    assert data == {"warning": 100, "danger": 100}


def test_save_thresholds_with_file_not_exist(tmp_path, monkeypatch):
    config_file = tmp_path / "non_exist.json"
    monkeypatch.setattr("main.CONFIG_FILE", str(config_file))
    data = load_thresholds()
    assert data == {"warning": 70, "danger": 90}

