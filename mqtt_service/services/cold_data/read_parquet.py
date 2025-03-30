import pandas as pd
from sklearn.ensemble import IsolationForest

# Path to your Parquet file
parquet_file_path = 'iot_device_data.parquet'  # Replace with your actual Parquet file path

# Read the Parquet file into a DataFrame
df = pd.read_parquet(parquet_file_path)

# Print the DataFrame in tabular format
print(df)

# Perform aggregation: group by a specific column and calculate the mean for another column
# Replace 'group_column' and 'value_column' with actual column names from your DataFrame
# aggregated_df = df.groupby('group_column')['value_column'].mean()

# Print the aggregated DataFrame
# print(aggregated_df)

# Calculate KPIs for sensor values
# Replace 'sensor_value_column' with the actual column name for sensor values
kpi = df['value'].agg(['min', 'max', 'mean', 'std'])

# Print the calculated KPIs
print("Sensor Value KPIs:")
print(kpi)

# Identify anomalies in sensor values
# Replace 'value' with the actual column name for sensor values
# Define thresholds for anomaly detection
lower_threshold = kpi['mean'] - 3 * kpi['std']
upper_threshold = kpi['mean'] + 3 * kpi['std']

# Filter rows where sensor values are outside the thresholds
anomalies = df[(df['value'] < lower_threshold) | (df['value'] > upper_threshold)]

# Print the anomalies
print("Anomalies in Sensor Values:")
print(anomalies)

# Predict anomalies using Isolation Forest
# Replace 'value' with the actual column name for sensor values
model = IsolationForest(contamination=0.05, random_state=42)
df['anomaly'] = model.fit_predict(df[['value']])

# Anomalies are marked as -1 by the model
predicted_anomalies = df[df['anomaly'] == -1]

# Print the predicted anomalies
print("Predicted Anomalies:")
print(predicted_anomalies)
