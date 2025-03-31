from opcua import Client
import paho.mqtt.client as mqtt
import json
import time

# OPC UA Server Configuration
OPC_SERVER_URL = "opc.tcp://localhost:4840/freeopcua/server/"  # Replace with your OPC UA server URL

# MQTT Broker Configuration
MQTT_BROKER = "localhost"  # Replace with your MQTT broker address
MQTT_PORT = 1883           # Default MQTT port
MQTT_TOPIC = "plc/data"    # MQTT topic to publish data

def read_opc_and_publish_to_mqtt():
    # Connect to the OPC UA server
    opc_client = Client(OPC_SERVER_URL)
    mqtt_client = mqtt.Client()

    try:
        print(f"Connecting to OPC UA server at {OPC_SERVER_URL}...")
        opc_client.connect()
        print("Connected to OPC UA server.")

        print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
        mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        print("Connected to MQTT broker.")

        # Get the root node of the OPC UA server
        root = opc_client.get_root_node()
        print(f"Root node: {root}")

        # Get the Objects node
        objects = opc_client.get_objects_node()
        print(f"Objects node: {objects}")

        # Access the "MyObject" node
        namespace_index = opc_client.get_namespace_index("http://localhost/opcua/")
        my_object_node = objects.get_child([f"{namespace_index}:MyObject"])
        print(f"MyObject node: {my_object_node}")

        # Access the Temperature and Humidity nodes
        temperature_node = my_object_node.get_child([f"{namespace_index}:Temperature"])
        humidity_node = my_object_node.get_child([f"{namespace_index}:Humidity"])
        print(f"Temperature node: {temperature_node}")
        print(f"Humidity node: {humidity_node}")

        # Continuously read data from OPC UA server and publish to MQTT
        while True:
            # Read values from OPC UA server
            temperature = temperature_node.get_value()
            humidity = humidity_node.get_value()
            print(f"Read from OPC UA server: Temperature={temperature}°C, Humidity={humidity}%")

            # Create a JSON payload
            payload = {
                "temperature": temperature,
                "humidity": humidity,
                "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime())
            }

            # Publish the data to MQTT
            mqtt_client.publish(MQTT_TOPIC, json.dumps(payload))
            print(f"Published to MQTT: {payload}")

            # Wait for a short interval before the next read
            time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Disconnect from OPC UA server and MQTT broker
        opc_client.disconnect()
        print("Disconnected from OPC UA server.")
        mqtt_client.disconnect()
        print("Disconnected from MQTT broker.")

if __name__ == "__main__":
    read_opc_and_publish_to_mqtt()