"""Flask web app for the Smart Battery Health Monitoring System."""
import csv
import io

from flask import Flask, jsonify, render_template, request, Response

from battery_monitor import BatteryMonitor
import config

app = Flask(__name__)
monitor = BatteryMonitor()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/telemetry")
def telemetry():
    return jsonify(monitor.get_reading())


@app.get("/api/history")
def history():
    try:
        limit = int(request.args.get("limit", 20))
    except ValueError:
        limit = 20
    return jsonify(monitor.get_history(limit))


@app.get("/api/export.csv")
def export_csv():
    # Ensure there is at least one record when the endpoint is used immediately.
    if not monitor.get_all_history():
        monitor.get_reading()
    rows = monitor.get_all_history()
    output = io.StringIO()
    fields = ["timestamp", "voltage_v", "current_a", "temperature_c", "soc_pct", "soh_pct", "status"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row.get(key, "") for key in fields})
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=battery-telemetry.csv"},
    )


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "smart-battery-health-monitor"})


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
