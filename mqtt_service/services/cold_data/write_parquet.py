import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
from influx_read import write_to_influx  # Import the function to write to InfluxDB

def json_to_parquet(json_data, output_file='iot_device_data.parquet'):
    # Flattening the JSON structure
    device = json_data["device"]
    sensor_data = json_data["sensor_data"]
    metadata = json_data["metadata"]

    # Flatten device information
    device_info = {
        "device_id": device["device_id"],
        "device_name": device["device_name"],
        "device_type": device["device_type"],
        "site": device["location"]["site"],
        "room": device["location"]["room"],
        "latitude": device["location"]["coordinates"]["latitude"],
        "longitude": device["location"]["coordinates"]["longitude"],
        "status": device["status"],
        "last_maintenance": device["last_maintenance"],
        "next_maintenance_due": device["next_maintenance_due"]
    }

    # Flatten sensor data (repeat for each sensor)
    sensor_info = []
    for sensor in sensor_data["data"]:
        sensor_info.append({
            "timestamp": sensor_data["timestamp"],
            "sensor_id": sensor["sensor_id"],
            "sensor_type": sensor["sensor_type"],
            "value": sensor["value"],
            "unit": sensor["unit"],
            "status": sensor["status"],
            "alarm_status": sensor["alarm"]["status"],
            "alarm_min_threshold": sensor["alarm"]["thresholds"]["min"],
            "alarm_max_threshold": sensor["alarm"]["thresholds"]["max"]
        })

    # Flatten metadata
    metadata_info = {
        "data_quality": metadata["data_quality"],
        "data_source": metadata["data_source"],
        "protocol": metadata["protocol"],
        "data_format": metadata["data_format"]
    }

    # Create DataFrames for device, sensor, and metadata information
    df_device = pd.DataFrame([device_info])
    df_sensor = pd.DataFrame(sensor_info)
    df_metadata = pd.DataFrame([metadata_info])

    # Merge data into a single DataFrame based on 'device_id'
    final_df = df_device.merge(df_sensor, how="cross").merge(df_metadata, how="cross")

    # Check if the output Parquet file already exists
    if os.path.exists(output_file):
        # If the file exists, append the new data to it
        existing_df = pd.read_parquet(output_file)
        final_df = pd.concat([existing_df, final_df], ignore_index=True)

    # Convert to PyArrow Table and write to Parquet
    table = pa.Table.from_pandas(final_df)

    # If the Parquet file exists, append, otherwise create a new file
    pq.write_table(table, output_file)
    
    print(f"Parquet file '{output_file}' has been created/updated successfully!")

    # Write the final DataFrame to InfluxDB
    write_to_influx(final_df)
    print("Data has been written to InfluxDB successfully!")

