import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Database and table info
DB_PATH = "informationUpload.db"  # Update with actual database path
TABLE_NAME = "alerts"  # Update with actual table name

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)

# SQL Query to fetch data
query = f"SELECT alert_time, duration, monitoring_server FROM {TABLE_NAME}"
df = pd.read_sql(query, conn)

# Convert 'alert_time' to datetime format
df["alert_time"] = pd.to_datetime(df["alert_time"])

# Extract only the date for aggregation
df["date"] = df["alert_time"].dt.date

# Aggregate: sum durations per location per day
grouped_df = df.groupby(["date", "monitoring_server"])["duration"].sum().unstack(fill_value=0)

# Close database connection
conn.close()

# Plot the stacked bar chart
grouped_df.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="tab10")

# Formatting
plt.xlabel("Date")
plt.ylabel("Total Outage Duration (seconds)")
plt.title("Stacked Bar Graph of Outage Duration by Location")
plt.xticks(rotation=45)  # Rotate date labels for readability
plt.legend(title="Location")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show the graph
plt.show()