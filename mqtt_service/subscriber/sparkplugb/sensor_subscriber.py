import paho.mqtt.client as mqtt
import base64
import sensor_pb2  # Import the generated Protobuf module
import json
import time

# MQTT Configuration
BROKER = "127.0.0.1"  # Change if needed
PORT = 1883
TOPIC = "spBv1.0/FactoryA/ProductionLine3/TemperatureHumidity"

def on_connect(client, userdata, flags, rc):
    """Callback when the client connects to the broker."""
    print(f"✅ Connected to MQTT Broker ({BROKER}) with result code {rc}")
    client.subscribe(TOPIC)
    print(f"📡 Subscribed to topic: {TOPIC}")

def on_message(client, userdata, msg):
    """Callback when a message is received."""
    try:
        # Decode JSON payload
        payload = json.loads(msg.payload.decode("utf-8"))
        
        # Extract metadata
        message_timestamp = payload.get("timestamp", 0)
        sequence_number = payload.get("seq", 0)

        print("\n📥 Received Sparkplug B v3 Message")
        print(f"🕒 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(message_timestamp / 1000))}")
        print(f"🔢 Sequence Number: {sequence_number}")

        # Process each metric
        for metric in payload.get("metrics", []):
            metric_name = metric.get("name", "Unknown")
            metric_alias = metric.get("alias", "N/A")

            print(f"\n📊 Metric: {metric_name} (Alias: {metric_alias})")

            # Extract and decode Base64-encoded Protobuf data
            encoded_data = metric.get("value", "")
            protobuf_bytes = base64.b64decode(encoded_data)

            # Deserialize Protobuf message
            sensor_data = sensor_pb2.SensorResponse()
            sensor_data.ParseFromString(protobuf_bytes)

            # Print parsed sensor data
            print(f"🔹 Device ID: {sensor_data.device_id}")
            print(f"🔹 Device Name: {sensor_data.device_name}")
            print(f"🔹 Status: {sensor_data.status}")
            print(f"🌡 Temperature: {sensor_data.temperature} {sensor_data.temperature_unit}")
            print(f"💧 Humidity: {sensor_data.humidity} {sensor_data.humidity_unit}")
            print(f"📍 Location: {sensor_data.site} - {sensor_data.room} ({sensor_data.latitude}, {sensor_data.longitude})")
            print("-" * 60)

    except Exception as e:
        print(f"❌ Error processing message: {e}")

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect and start loop
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_forever()
