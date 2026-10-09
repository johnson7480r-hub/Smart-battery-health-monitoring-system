"""Demo settings. Adapt these to your battery chemistry and pack specifications."""

HOST = "127.0.0.1"
PORT = 5000
DEBUG = False

NOMINAL_CAPACITY_AH = 20.0

# Generic demonstration thresholds only; do not use as safety limits without validation.
LOW_VOLTAGE_V = 10.8
HIGH_VOLTAGE_V = 14.8
HIGH_TEMPERATURE_C = 45.0
CRITICAL_TEMPERATURE_C = 55.0
LOW_SOC_PCT = 20.0
LOW_SOH_PCT = 70.0

HISTORY_LIMIT = 300
