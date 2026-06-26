import json
import paho.mqtt.client as mqtt

host = "b792c9ff.ala.asia-southeast1.emqxsl.com"
port = 8084
topic = "pv/data"
username = "Rsi123"  # Catatan: Ingat untuk segera mengubah password rapuh ini di EMQX
password = "Rsi123"
client_id = "test-publish-client"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker successfully! (Code:", rc, ")")
        payload = json.dumps({
            "lux": 350,
            "temperature": 38.5,
            "voltage": 16.8,
            "current": 1.95,
            "power": 42.2,
            "condition": "shaded",
            "timestamp": "2026-06-25T15:00:00Z"
        })
        # QoS=1 menjamin pesan setidaknya sampai satu kali ke broker
        client.publish(topic, payload, qos=1) 
        print("Published payload:", payload)
        client.disconnect() # Memutuskan koneksi dengan bersih setelah tugas selesai
    else:
        print("Failed to connect. Return code:", rc)

client = mqtt.Client(client_id=client_id, transport="websockets")
client.username_pw_set(username, password)
client.tls_set()  # Wajib untuk port 8084 (Secure)
client.on_connect = on_connect

print("Attempting to connect...")
client.connect(host, port)
client.loop_forever() # Akan berhenti otomatis karena ada client.disconnect() di atas