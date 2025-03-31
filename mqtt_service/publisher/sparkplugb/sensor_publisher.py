import time
import json
import base64
import paho.mqtt.client as mqtt
import sensor_pb2  # Import the generated Protobuf module
import datetime  # Import datetime module for UTC conversion
import sys  # Import sys to handle command-line arguments

# MQTT Configuration
BROKER = "127.0.0.1"  # Change to your MQTT broker address
PORT = 1883
TOPIC = "spBv1.0/FactoryA/ProductionLine3/TemperatureHumidity"

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()

# Sequence number for Sparkplug messages
sequence_number = 0

def generate_sensor_data(temperature, humidity):
    """Generates sensor data and encodes it using Protobuf."""
    sensor_data = sensor_pb2.SensorResponse(
        device_id="device_001",
        device_name="Temperature_Humidity_Sensor",
        device_type="Sensor",
        status="active",
        last_maintenance="2025-02-15T10:30:00Z",
        next_maintenance_due="2025-08-15T10:30:00Z",
        temperature=temperature,
        temperature_unit="A",
        humidity=humidity,
        humidity_unit="%",
        site="Factory A",
        room="Production Line 3",
        latitude=37.7749,
        longitude=-122.4194
    )
    return sensor_data

def publish_sensor_data(temperature, humidity):
    global sequence_number
    
    # Generate sensor data
    sensor_data = generate_sensor_data(temperature, humidity)

    # Serialize to Protobuf
    protobuf_payload = sensor_data.SerializeToString()

    # Encode in Base64 for MQTT
    encoded_payload = base64.b64encode(protobuf_payload).decode('utf-8')
    print(f"Encoded Payload: {encoded_payload}")

    # Convert current timestamp to UTC ISO 8601 format
    utc_timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    # Sparkplug B v3 message format
    sparkplug_message = {
        "timestamp": int(time.time() * 1000),
        "metrics": [
            {
                "name": "sensor_data",
                "alias": 1,
                "timestamp": int(time.time() * 1000),
                "dataType": "byteArray",  # Base64-encoded Protobuf
                "value": encoded_payload
            }
        ],
        "seq": sequence_number
    }

    # Convert to JSON
    json_message = json.dumps(sparkplug_message)

    # Publish the message
    mqtt_client.publish(TOPIC, json_message)
    print(f"✅ Published Sparkplug B v3 Message: {json_message}")

    # Increment sequence number
    sequence_number += 1

if __name__ == "__main__":
    # Ensure the script is called with the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python sensor_publisher.py <temperature> <humidity>")
        sys.exit(1)

    # Parse the temperature and humidity arguments
    try:
        temperature = float(sys.argv[1])
        humidity = float(sys.argv[2])
    except ValueError:
        print("Error: Temperature and Humidity must be numeric values.")
        sys.exit(1)

    try:
        # Publish the sensor data
        publish_sensor_data(temperature, humidity)
    except KeyboardInterrupt:
        print("MQTT Publisher Stopped")
    finally:
        mqtt_client.loop_stop()