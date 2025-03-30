import paho.mqtt.client as mqtt
import base64
import json

# Define the MQTT callback functions

def on_connect(client, userdata, flags, rc):
    """Callback function when the client connects to the broker."""
    print(f"Connected with result code {rc}")
    # Subscribe to the Sparkplug B topic when connected
    client.subscribe("spBv1.0/FactoryA/ProductionLine3/TemperatureHumidity")

def on_message(client, userdata, msg):
    """Callback function when a message is received on a subscribed topic."""
    try:
        # Decode the base64-encoded payload
        decoded_message = base64.b64decode(msg.payload).decode('utf-8')

        # Parse the decoded message (which should be a JSON string)
        iot_data = json.loads(decoded_message)

        # Print the decoded and parsed message
        print(f"Received decoded message: {iot_data} on topic '{msg.topic}'")
    
    except Exception as e:
        print(f"Error decoding message: {e}")

# Create a new MQTT client instance
client = mqtt.Client()

# Attach the callback functions to the client
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker (you can change the broker and port to your own)
broker = "127.0.0.1"  # You can replace this with your broker's IP or domain
port = 1883  # Standard MQTT port
client.connect(broker, port, 60)  # Connect to the broker with keepalive time of 60 seconds

# Start the MQTT client loop to listen for messages (this will block the program)
client.loop_forever()
