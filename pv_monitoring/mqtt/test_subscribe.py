import json
import paho.mqtt.client as mqtt

host = "b792c9ff.ala.asia-southeast1.emqxsl.com"
port = 8084
topic = "pv/data"
username = "Rsi123"
password = "Rsi123"
client_id = "test-subscribe-client"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker successfully! (Code:", rc, ")")
        print("Subscribing to topic:", topic)
        client.subscribe(topic, qos=1)
    else:
        print("Failed to connect. Return code:", rc)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        print("\nReceived message on topic:", msg.topic)
        print(payload)
        data = json.loads(payload)
        print("Parsed JSON:", json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print("Failed to decode message:", e)


def on_disconnect(client, userdata, rc):
    print("Disconnected from broker (Code:", rc, ")")


client = mqtt.Client(client_id=client_id, transport="websockets")
client.username_pw_set(username, password)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

print("Attempting to connect to MQTT Cloud...")
client.connect(host, port)
client.loop_forever()