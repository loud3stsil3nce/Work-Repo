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





# Function to export any table to CSV
# def export_table_to_csv(table_name, csv_filename):
#     try:
#         cursor.execute(f"SELECT * FROM {table_name}")
#         data = cursor.fetchall()

#         # Get column names
#         column_names = [desc[0] for desc in cursor.description]

#         # Write to CSV file
#         with open(csv_filename, "w", newline="", encoding="utf-8") as file:
#             writer = csv.writer(file)
#             writer.writerow(column_names)  # Write header
#             writer.writerow("")
#             writer.writerows(data)  # Write data

#         print(f"✅ {table_name} data saved to {csv_filename}")

#     except sqlite3.OperationalError:
#         print(f"❌ Table '{table_name}' does not exist in the database.")

# # Export tables
# export_table_to_csv("outages", "outages_report.csv")
# export_table_to_csv("alerts", "alerts_report.csv")

# Close database connection
