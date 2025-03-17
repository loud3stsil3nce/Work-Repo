import requests
import json
import csv
import sqlite3
from OutageRetrieval import outages 

conn = sqlite3.connect("informationUpload.db")
cursor = conn.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
        
        
        id INTEGER PRIMARY KEY,
        outage_id INTEGER,
        location TEXT,
        monitoring_server TEXT,
        ipv4 TEXT,
        alert_time TEXT,
        duration INTEGER,
        output TEXT,
        FOREIGN KEY (outage_id) REFERENCES outages (id)
   )
 """)



 # Insert data
for outage in outages:
    # cursor.execute("INSERT INTO alerts VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
    #     outage["pk"],
    #     outage["check_name"],
    #     outage["check_address"],
    #     outage["created_at"],
    #     outage["resolved_at"],
        
    #     outage["num_locations_down"]
    # ))
    for alert in outage.get("all_alerts", []):  # Use .get() to avoid KeyErrors
         cursor.execute("INSERT INTO alerts VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
             alert["pk"],
             outage["pk"],  # Link alert to outage
             alert["location"],
             alert["monitoring_server_name"],
             alert["monitoring_server_ipv4"],
             alert["created_at"],
             outage["duration_secs"],
             alert["output"]
         ))

conn.commit()
conn.close()

