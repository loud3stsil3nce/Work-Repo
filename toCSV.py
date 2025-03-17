import sqlite3
import pandas as pd

def export_table_to_csv(db_path, table_name, output_csv):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Read table into a DataFrame
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    # Save DataFrame to CSV
    df.to_csv(output_csv, index=False)

    # Close the connection
    conn.close()
    print(f"✅ Exported '{table_name}' to '{output_csv}'")

# Usage Example
db_path = "informationUpload.db"  # Change this to your actual database file
table_name = "alerts"  # Change this to the table you want to export
output_csv = "alertinfo.csv"  # Change this to your desired CSV filename

export_table_to_csv(db_path, table_name, output_csv)