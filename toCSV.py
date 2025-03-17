import sqlite3, csv
import pandas as pd

def export_table_to_csv(db_path, table_name, output_file):
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch all rows from the table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Get column names
    column_names = [desc[0] for desc in cursor.description]
    
    # Write to CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)  # Ensure proper CSV formatting
        writer.writerow(column_names)  # Write header
        
        for row in rows:
            # Convert row to list to modify it
            row = list(row)
            # Fix newlines in text columns (replace "\n" with space)
            row = [str(value).replace("\n", " ") if isinstance(value, str) else value for value in row]
            writer.writerow(row)

    # Close connection
    conn.close()
    print(f"✅ Exported '{table_name}' to '{output_file}' with corrected formatting!")



db_path = "informationUpload.db"  # Change this to your actual database file
table_name = "alerts"  # Change this to the table you want to export
output_csv = "alertinfo.csv"  # Change this to your desired CSV filename

export_table_to_csv(db_path, table_name, output_csv)