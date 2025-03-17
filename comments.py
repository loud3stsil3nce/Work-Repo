
# with open("alerts_report.csv", "w", newline="") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Alert ID", "Outage ID", "Service", "Location", "Monitoring Server", "IPv4", "Alert Time", "Error"])

#     for outage in outages:
#         for alert in outage.get("all_alerts", []):
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

# print("Alerts saved to alerts_report.csv")

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
