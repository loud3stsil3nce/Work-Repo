import requests
import json
import csv
import sqlite3

url = "https://uptime.com/api/v1/outages/?format=json"
headers = {
    "Authorization": "Token a3a284cc5c531761437181941aba7ff8fc015a3c",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    outages = response.json()
    print(outages)
else:
    print(f"Error: {response.status_code} - {response.text}")


if isinstance(outages, str):  # If outages is still a string, convert it to a dictionary
    outages = json.loads(outages)
if isinstance(outages, dict) and "results" in outages:
    outages = outages["results"]

print(json.dumps(outages, indent=4))
for outage in outages:
    print(f"Outage ID: {outage['pk']}")
    print(f"Service Affected: {outage['check_name']} ({outage['check_address']})")
    print(f"Start Time: {outage['created_at']}")
    print(f"Resolved Time: {outage['resolved_at']}")
    print(f"Duration: {outage['duration_secs']} seconds")
    print(f"Number of locations affected: {outage['num_locations_down']}")
    
    print("\n⚠️ Alerts Associated with This Outage:")
    for alert in outage.get("all_alerts", []):
        print(f"  🔹 Alert ID: {alert['pk']}")
        print(f"  📍 Location: {alert['location']}")
        print(f"  🖥️ Server: {alert['monitoring_server_name']} ({alert['monitoring_server_ipv4']})")
        print(f"  📅 Alert Time: {alert['created_at']}")
        print(f"  🚨 Error: {alert['output'].splitlines()[0]}")
        print("  ----------------------------------------")

    print("\n" + "="*50 + "\n")



with open("alerts_report.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Alert ID", "Outage ID", "Service", "Location", "Monitoring Server", "IPv4", "Alert Time", "Error"])

    for outage in outages:
        for alert in outage.get("all_alerts", []):
            writer.writerow([
                alert["pk"],
                outage["pk"],
                outage["check_name"],
                alert["location"],
                alert["monitoring_server_name"],
                alert["monitoring_server_ipv4"],
                alert["created_at"],
                alert["output"].splitlines()[0]
            ])

print("Alerts saved to alerts_report.csv")

# conn = sqlite3.connect("outages.db")
# cursor = conn.cursor()

# # Create table
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS outages (
#         id INTEGER PRIMARY KEY,
#         service TEXT,
#         address TEXT,
#         start_time TEXT,
#         resolved_time TEXT,
#         duration INTEGER,
#         locations_down INTEGER
#     )
# """)



# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS alerts (
#         id INTEGER PRIMARY KEY,
#         outage_id INTEGER,
#         location TEXT,
#         monitoring_server TEXT,
#         ipv4 TEXT,
#         alert_time TEXT,
#         output TEXT,
#         FOREIGN KEY (outage_id) REFERENCES outages (id)
#     )
# """)

# Insert data
#for outage in outages:
    # cursor.execute("INSERT INTO outages VALUES (?, ?, ?, ?, ?, ?, ?)", (
    #     outage["pk"],
    #     outage["check_name"],
    #     outage["check_address"],
    #     outage["created_at"],
    #     outage["resolved_at"],
    #     outage["duration_secs"],
    #     outage["num_locations_down"]
    # ))
#     for alert in outage.get("all_alerts", []):  # Use .get() to avoid KeyErrors
#         cursor.execute("INSERT INTO alerts VALUES (?, ?, ?, ?, ?, ?, ?)", (
#             alert["pk"],
#             outage["pk"],  # Link alert to outage
#             alert["location"],
#             alert["monitoring_server_name"],
#             alert["monitoring_server_ipv4"],
#             alert["created_at"],
#             alert["output"]
#         ))

# conn.commit()
# conn.close()

# print("Data stored in outages.db")





# Connect to SQLite database
conn = sqlite3.connect("outages.db")
cursor = conn.cursor()

# Fetch all alert records
cursor.execute("SELECT * FROM alerts")
alerts_data = cursor.fetchall()

# Get column names
column_names = [desc[0] for desc in cursor.description]

# Write to CSV
csv_filename = "alerts_report.csv"
with open(csv_filename, "w", newline="") as file:
    writer = csv.writer(file)
    
    writer.writerow(column_names)
      # Write header
    writer.writerows(alerts_data)  # Write data

# Close database connection
conn.close()

print(f"✅ Alerts data saved to {csv_filename}")





# conn = sqlite3.connect("alerts.db")
# cursor = conn.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS alerts (
#         id INTEGER PRIMARY KEY,
#         outage_id INTEGER,
#         location TEXT,
#         monitoring_server TEXT,
#         ipv4 TEXT,
#         alert_time TEXT,
#         output TEXT,
#         FOREIGN KEY (outage_id) REFERENCES outages (id)
#     )
# """)



# # Insert data
# for outage in outages:
#     # cursor.execute("INSERT INTO outages VALUES (?, ?, ?, ?, ?, ?, ?)", (
#     #     outage["pk"],
#     #     outage["check_name"],
#     #     outage["check_address"],
#     #     outage["created_at"],
#     #     outage["resolved_at"],
#     #     outage["duration_secs"],
#     #     outage["num_locations_down"]
#     # ))
#      for alert in outage.get("all_alerts", []):  # Use .get() to avoid KeyErrors
#          cursor.execute("INSERT INTO alerts VALUES (?, ?, ?, ?, ?, ?, ?)", (
#              alert["pk"],
#              outage["pk"],  # Link alert to outage
#              alert["location"],
#              alert["monitoring_server_name"],
#              alert["monitoring_server_ipv4"],
#              alert["created_at"],
#              alert["output"]
#          ))

# conn.commit()
# conn.close()


# with open("alerts_report_fixed.csv", "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Alert ID", "Outage ID", "Service", "Location", "Monitoring Server", "IPv4", "Alert Time", "Error"])
#     for alert in alerts:
#         for alert in alert.get("all_alerts", []):
#             writer.writerow([
#                 alert["pk"],
#                 outage["pk"],
#                 outage["check_name"],
#                 alert["location"],
#                 alert["monitoring_server_name"],
#                 alert["monitoring_server_ipv4"],
#                 alert["created_at"],
#                 alert["output"].splitlines()[0]
#             ])

#         writer.writerows(data)  # Write data



conn = sqlite3.connect("outages.db")
cursor = conn.cursor()

# Function to export any table to CSV
def export_table_to_csv(table_name, csv_filename):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()

        # Get column names
        column_names = [desc[0] for desc in cursor.description]

        # Write to CSV file
        with open(csv_filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(column_names)  # Write header
            writer.writerow("")
            writer.writerows(data)  # Write data

        print(f"✅ {table_name} data saved to {csv_filename}")

    except sqlite3.OperationalError:
        print(f"❌ Table '{table_name}' does not exist in the database.")

# Export tables
export_table_to_csv("outages", "outages_report.csv")
export_table_to_csv("alerts", "alerts_report.csv")

# Close database connection
conn.close()