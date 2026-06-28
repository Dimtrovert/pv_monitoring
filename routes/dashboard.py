from flask import Blueprint, render_template, current_app, jsonify, request
from database.models import PVData
from datetime import datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__)

from flask import Blueprint, render_template, current_app, jsonify, request, session, redirect

from database.models import PVData
from datetime import datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard():
    # KUNCI KEAMANAN: Cek apakah user memiliki tiket masuk (session)
    if not session.get("logged_in"):
        return redirect("/auth/login") # Tendang ke halaman login jika tidak ada

    return render_template(
        "dashboard.html",
        mqtt_config={
            "host": current_app.config.get("MQTT_WS_HOST"),
            "port": current_app.config.get("MQTT_WS_PORT"),
            "path": current_app.config.get("MQTT_WS_PATH"),
            "topic": current_app.config.get("MQTT_TOPIC"),
            "username": current_app.config.get("MQTT_USERNAME"),
            "password": current_app.config.get("MQTT_PASSWORD"),
            "useSSL": current_app.config.get("MQTT_USE_SSL", True)
        }
    )

# ... (biarkan rute /api/historical-data di bawahnya tetap seperti semula)
@dashboard_bp.route("/api/historical-data")
def historical_data():
    try:
        period = request.args.get('period', '1h')
        
        # SOLUSI ANTI-AMNESIA: Patokan waktu bukan dari laptop, tapi dari Data Paling Akhir di Supabase
        latest_record = PVData.query.order_by(PVData.timestamp.desc()).first()
        
        if not latest_record:
            # Jika database benar-benar kosong
            return jsonify({"labels": [], "voltage": [], "power": [], "lux": [], "temperature": [], "current": []})
            
        latest_time = latest_record.timestamp

        # Tarik mundur dari waktu record terakhir
        if period == '1h':
            time_threshold = latest_time - timedelta(hours=1)
        elif period == '1d':
            time_threshold = latest_time - timedelta(days=1)
        elif period == '7d':
            time_threshold = latest_time - timedelta(days=7)
        else:
            time_threshold = latest_time - timedelta(hours=1)

        records = PVData.query.filter(PVData.timestamp >= time_threshold)\
                              .order_by(PVData.timestamp.asc()).all()

        # DOWNSAMPLING: Cegah browser hang jika data berjumlah ribuan
        max_points = 100
        if len(records) > max_points:
            step = len(records) // max_points
            records = records[::step]

        data_grafik = {
            "labels": [], "voltage": [], "power": [], 
            "lux": [], "temperature": [], "current": []
        }

        for row in records:
            # KUNCI: Ubah ke format ISO dengan huruf 'Z' (ZULU/UTC) di belakangnya.
            # Ini akan memaksa Javascript di Frontend mengubahnya sendiri ke zona waktu lokal Anda (WIB).
            waktu_iso = row.timestamp.isoformat() + "Z" if row.timestamp else ""
            data_grafik["labels"].append(waktu_iso)
            
            data_grafik["voltage"].append(row.voltage)
            data_grafik["power"].append(row.power)
            data_grafik["lux"].append(row.lux)
            data_grafik["temperature"].append(row.temperature)
            data_grafik["current"].append(row.current)

        return jsonify(data_grafik)

    except Exception as e:
        return jsonify({"error": str(e)}), 500