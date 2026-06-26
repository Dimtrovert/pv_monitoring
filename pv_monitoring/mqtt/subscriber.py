import json
import paho.mqtt.client as mqtt
from database.db import db
from database.models import PVData

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Backend Subscriber Connected to EMQX Broker! 🟢")
        topic = userdata.get("topic")
        if topic:
            client.subscribe(topic)
            print(f"Mendengarkan topik: {topic}")
    else:
        print(f"Gagal terhubung ke EMQX, kode: {reason_code}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(f"\nBackend menerima data dari EMQX: {payload}")

        app = userdata.get("app")

        with app.app_context():
            new_data = PVData(
                lux=payload.get("lux", 0),
                temperature=payload.get("temperature", 0),
                voltage=payload.get("voltage", 0),
                current=payload.get("current", 0),
                power=payload.get("power", 0),
                condition=payload.get("condition", "unknown"),
                # KUNCI BARU: Menangkap nilai Confidence
                confidence=payload.get("confidence", 0.0)
            )
            db.session.add(new_data)
            db.session.commit()
            print("✅ Data berhasil diukir ke Supabase PostgreSQL!")

    except Exception as e:
        print(f"🔴 Error Database/Parsing: {e}")

def start_mqtt(app):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.user_data_set({
        "app": app,
        "topic": app.config.get("MQTT_TOPIC", "pv/data")
    })

    client.username_pw_set(app.config["MQTT_USERNAME"], app.config["MQTT_PASSWORD"])
    client.tls_set()

    print("Mencoba menyalakan mesin penyedot data...")
    client.connect(app.config["MQTT_WS_HOST"], 8883)
    
    client.loop_start()
    return client