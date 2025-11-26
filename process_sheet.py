import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# Load secrets
creds_json = os.environ.get("GOOGLE_CREDENTIALS")
sheet_id = os.environ.get("SHEET_ID")

# Write creds to file
with open("creds.json", "w") as f:
    f.write(creds_json)

# Authenticate
scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
gc = gspread.authorize(creds)

# Try to read the sheet
try:
    sheet = gc.open_by_key(sheet_id).sheet1
    data = sheet.get_all_records()
    print(f"Fetched {len(data)} rows from the sheet.")
except Exception as e:
    print("Error accessing sheet:", e)
    data = []

# Save JSON
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Generate HTML table
html = "<h2>Gig Graph Data</h2>\n"
html += """
<style>
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #f2f2f2; }
</style>
"""

if data:
    columns = data[0].keys()
    html += "<table><thead><tr>"
    for col in columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    for row in data:
        html += "<tr>"
        for col in columns:
            html += f"<td>{row[col]}</td>"
        html += "</tr>"
    html += "</tbody></table>"
else:
    html += "<p>No data available</p>"

with open("output.html", "w") as f:
    f.write(html)

print("output.html generated successfully.")
