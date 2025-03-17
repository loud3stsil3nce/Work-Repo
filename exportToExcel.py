import sqlite3
import pandas as pd

def export_table_to_excel(db_path, table_name, output_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Read table into a DataFrame
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    # Save DataFrame to Excel
    df.to_excel(output_file, index=False, engine='openpyxl')

    # Close the connection
    conn.close()
    print(f"✅ Exported '{table_name}' to '{output_file}'")

# Usage Example
db_path = "informationUpload.db"  # Change this to your SQLite database file
table_name = "alerts"  # Change this to the table you want to export
output_file = "alertData.xlsx"  # Change this to your desired Excel filename

export_table_to_excel(db_path, table_name, output_file)