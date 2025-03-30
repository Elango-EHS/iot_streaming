import time
import paho.mqtt.client as mqtt
import json
import base64  # For encoding the message to base64
import mqtt_service.publisher.sparkplugb.iot_data as iot_data  # Import the iot_data module


# Define the MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to the topic "test/iot" when connected (optional, not necessary here)
    # client.subscribe("test/iot")  # Uncomment if you need to subscribe to receive messages

def on_publish(client, userdata, mid):
    print(f"test_mqtt_iot Published : {mid}")

# Create a new MQTT client
client = mqtt.Client()

# Attach the callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker (use the appropriate broker IP or domain)
broker = "127.0.0.1"  # Replace with your broker IP
port = 1883  # Standard MQTT port
client.connect(broker, port, 60)
print("Sending messages to topic 'test_mqtt_iot'...")

# Start the MQTT client loop (non-blocking)
client.loop_start()

try:
    message_counter = 0
    while True:
        
        # Sparkplug-B payload structure
        sparkplug_message = {
            "timestamp": int(time.time() * 1000),  # Epoch time in milliseconds
            "metrics": [
                {
                    "name": "temprature",
                    "alias": 1,
                    "value": iot_data.generateTemprature(),  # Updated method name
                    "datatype": "float",
                    "unit": "C"
                },
                {
                    "name": "humidity",
                    "alias": 2,
                    "value": iot_data.generateHumidity(),  # Updated method name
                    "datatype": "float",
                    "unit": "%"
                }
            ],
            "device": {
                "id": iot_data.getRandomDeviceID(),  # Updated method name
                "name": "Temperature_Humidity_Sensor",
                "type": "Sensor",
                "status": "active"
            },
            "location": {
                "site": iot_data.getRandomSiteName(),  # Updated method name
                "room": iot_data.getRandomRoomName(),  # Updated method name
                "coordinates": iot_data.getRandomCoordinates()  # Directly use the dictionary
            }
        }

        # Convert the Sparkplug-B message to a JSON string
        json_message = json.dumps(sparkplug_message)

        # Encode the JSON message to base64
        encoded_message = base64.b64encode(json_message.encode('utf-8'))
        print(f"Generated Sparkplug-B IoT data: {json_message}")

        # Publish the base64 encoded message to the topic "spBv1.0/FactoryA/ProductionLine3/TemperatureHumidity"
        client.publish("spBv1.0/FactoryA/ProductionLine3/TemperatureHumidity", encoded_message)

        # Increment the message counter
        message_counter += 1
        print(f"Message {message_counter} sent to topic 'spBv1.0/FactoryA/ProductionLine3/TemperatureHumidity'")

        # Wait for 1 second before sending the next message
        time.sleep(1)

except KeyboardInterrupt:
    print("Publisher stopped manually.")
    # Stop the loop when the program is interrupted
    client.loop_stop()
