"""Battery telemetry source and health/alert helpers.

The default source is simulated. Replace it with a validated BMS/sensor adapter
for real hardware; never treat these demo estimates as safety instrumentation.
"""
from collections import deque
from datetime import datetime, timezone
import random
import threading

import config


class SimulatedBatterySource:
    """Generate plausible-looking demo telemetry without external hardware."""

    def __init__(self):
        self._lock = threading.Lock()
        self._soc = 86.0
        self._soh = 96.0
        self._tick = 0

    def read(self):
        with self._lock:
            self._tick += 1
            # Slowly drain the simulated battery and very slowly age its capacity.
            self._soc = max(0.0, self._soc - random.uniform(0.02, 0.12))
            if self._tick % 100 == 0:
                self._soh = max(60.0, self._soh - 0.1)

            voltage = 10.5 + (self._soc / 100.0) * 3.9 + random.uniform(-0.08, 0.08)
            current = random.uniform(0.4, 2.5)
            temperature = 29.0 + random.uniform(-2.0, 8.0)
            return {
                "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "voltage_v": round(voltage, 2),
                "current_a": round(current, 2),
                "temperature_c": round(temperature, 1),
                "soc_pct": round(self._soc, 1),
                "soh_pct": round(self._soh, 1),
            }


class BatteryMonitor:
    def __init__(self, source=None, history_limit=None):
        self.source = source or SimulatedBatterySource()
        self.history = deque(maxlen=history_limit or config.HISTORY_LIMIT)
        self._lock = threading.Lock()

    def get_reading(self):
        reading = self.source.read()
        reading["alerts"] = self.evaluate_alerts(reading)
        reading["status"] = self.status_from_alerts(reading["alerts"])
        with self._lock:
            self.history.append(reading.copy())
        return reading

    @staticmethod
    def evaluate_alerts(reading):
        alerts = []
        if reading["voltage_v"] < config.LOW_VOLTAGE_V:
            alerts.append({"level": "critical", "message": "Battery voltage is below the configured minimum."})
        elif reading["voltage_v"] > config.HIGH_VOLTAGE_V:
            alerts.append({"level": "warning", "message": "Battery voltage is above the configured maximum."})

        temp = reading["temperature_c"]
        if temp >= config.CRITICAL_TEMPERATURE_C:
            alerts.append({"level": "critical", "message": "Battery temperature is critically high."})
        elif temp >= config.HIGH_TEMPERATURE_C:
            alerts.append({"level": "warning", "message": "Battery temperature is high."})

        if reading["soc_pct"] <= config.LOW_SOC_PCT:
            alerts.append({"level": "warning", "message": "State of Charge is low."})
        if reading["soh_pct"] <= config.LOW_SOH_PCT:
            alerts.append({"level": "warning", "message": "Estimated State of Health is low."})
        return alerts

    @staticmethod
    def status_from_alerts(alerts):
        if any(alert["level"] == "critical" for alert in alerts):
            return "Critical"
        if alerts:
            return "Warning"
        return "Normal"

    def get_history(self, limit=20):
        with self._lock:
            return list(self.history)[-max(1, min(int(limit), config.HISTORY_LIMIT)):]

    def get_all_history(self):
        with self._lock:
            return list(self.history)
