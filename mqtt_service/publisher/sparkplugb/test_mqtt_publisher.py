from opcua import Client
import subprocess
import time

# OPC UA Server Configuration
OPC_SERVER_URL = "opc.tcp://localhost:4840/freeopcua/server/"  # Replace with your OPC UA server URL

def read_opc_and_send_to_sensor_publisher():
    # Connect to the OPC UA server
    opc_client = Client(OPC_SERVER_URL)

    try:
        # Connect to OPC UA server
        print(f"Connecting to OPC UA server at {OPC_SERVER_URL}...")
        opc_client.connect()
        print("Connected to OPC UA server.")

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

        # Continuously read data from OPC UA server and send to sensor_publisher.py
        while True:
            try:
                # Read values from OPC UA server
                temperature = temperature_node.get_value()
                humidity = humidity_node.get_value()
                
                print(f"Temperature Stats from OPC={temperature}°C, Humidity={humidity}%")
                # Call sensor_publisher.py with temperature and humidity as arguments
                subprocess.run(
                    ["python", "sensor_publisher.py", str(temperature), str(humidity)],
                    check=True
                )
                print(f"Published : Temperature Stats={temperature}, Humidity={humidity}")

                # Wait for a short interval before the next read
                time.sleep(0.01)

            except Exception as e:
                print(f"Error reading from OPC UA server: {e}")
                print("Attempting to reconnect...")
                try:
                    opc_client.disconnect()
                except Exception as e:
                    print(f"Error during disconnection: {e}")
                time.sleep(5)  # Wait before attempting to reconnect
                opc_client.connect()
                print("Reconnected to OPC UA server.")

    except Exception as e:
        print(f"Failed to connect to OPC UA server: {e}")

    finally:
        # Ensure proper disconnection
        try:
            opc_client.disconnect()
            print("Disconnected from OPC UA server.")
        except Exception as e:
            print(f"Error during disconnection: {e}")

if __name__ == "__main__":
    read_opc_and_send_to_sensor_publisher()