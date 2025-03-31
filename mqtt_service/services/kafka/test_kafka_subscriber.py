import base64
import json
import time
from confluent_kafka import Consumer, KafkaException, KafkaError
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import sensor_pb2  # Import the generated Protobuf module
# Configuration for Kafka Consumer
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    'group.id': 'my_consumer_group',        # Consumer group ID
    'auto.offset.reset': 'earliest'         # Start consuming from the earliest message
}

# Create Kafka consumer instance
consumer = Consumer(conf)

# The topic you want to consume messages from
topic = 'test-iot-topic'

# Subscribe to the topic
consumer.subscribe([topic])
print('Poll for new messages')

# Configuration for InfluxDB
influxdb_url = "http://localhost:8086"
influxdb_token = "mvmKmiT_b6hNSEvEYZKT2dhqnVsSq5mXoDsztOwrESzcOs6Fr5xpAO6hxZoeH4nW_0Ttvr46pAKkc4dppuSNAQ=="
influxdb_org = "ehs"
influxdb_bucket = "iot"

# Initialize InfluxDB client
influx_client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Timeout in seconds

        if msg is None:
            print('No Messages Received')
            continue
        if msg.error():
            # Handle errors
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"End of partition reached {msg.topic()} [{msg.partition}] at offset {msg.offset()}")
            else:
                raise KafkaException(msg.error())
        else:
            # Successfully received message
            try:
                # Debug raw Kafka message
                print(f"Message topic: {msg.topic()}")
                print(f"Message partition: {msg.partition()}")
                print(f"Message offset: {msg.offset()}")
                print(f"Message key: {msg.key()}")
                print(f"Message value: {msg.value()}")

                # Parse the JSON payload
                payload = json.loads(msg.value().decode("utf-8"))
                print(f"Parsed payload: {payload}")

                # Extract metadata
                message_timestamp = payload.get("timestamp", 0)
                sequence_number = payload.get("seq", 0)

                # Extract and decode Base64-encoded Protobuf data from the metrics
                metrics = payload.get("metrics", [])
                for metric in metrics:
                    encoded_data = metric.get("value", "")
                    if not encoded_data:
                        print("No encoded data found in metric, skipping...")
                        continue

                    # Decode Base64-encoded Protobuf data
                    protobuf_bytes = base64.b64decode(encoded_data)

                    # Deserialize Protobuf message
                    sensor_data = sensor_pb2.SensorResponse()
                    sensor_data.ParseFromString(protobuf_bytes)  # Deserialize the message
                    print(f"Decoded Protobuf message: {sensor_data}")

                    # Convert Protobuf message to a dictionary
                    decoded_message = {
                        "device_id": sensor_data.device_id,
                        "device_name": sensor_data.device_name,
                        "device_type": sensor_data.device_type,
                        "status": sensor_data.status,
                        "last_maintenance": sensor_data.last_maintenance,
                        "next_maintenance_due": sensor_data.next_maintenance_due,
                        "temperature": sensor_data.temperature,
                        "temperature_unit": sensor_data.temperature_unit,
                        "humidity": sensor_data.humidity,
                        "humidity_unit": sensor_data.humidity_unit,
                        "site": sensor_data.site,
                        "room": sensor_data.room,
                        "latitude": sensor_data.latitude,
                        "longitude": sensor_data.longitude,
                    }
                    print(f"Decoded message: {decoded_message}")

                    # Insert the JSON into InfluxDB
                    point = Point("iot_data").tag("source", "kafka").field("data", json.dumps(decoded_message))
                    write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
                    print("Inserted JSON into InfluxDB")

            except Exception as e:
                print(f"Error processing message: {e}")
                continue

except KeyboardInterrupt:
    print("Consumer interrupted, closing...")

finally:
    # Close the InfluxDB client
    influx_client.close()
    # Close the consumer gracefully
    consumer.close()
