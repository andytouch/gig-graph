import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime

# Load secrets
creds_json = os.environ["GOOGLE_CREDENTIALS"]
sheet_id = os.environ["SHEET_ID"]

# Write credentials to file
with open("creds.json", "w") as f:
    f.write(creds_json)

# Authenticate
scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
gc = gspread.authorize(creds)

# Open the sheet
sheet = gc.open_by_key(sheet_id).sheet1
data = sheet.get_all_records()

# Ensure first column is date and format it as YYYY-MM-DD
first_col = list(data[0].keys())[0] if data else None
for row in data:
    if first_col and row.get(first_col):
        # Try parsing date if possible
        try:
            dt = datetime.strptime(str(row[first_col]), "%Y-%m-%d")
            row[first_col] = dt.strftime("%Y-%m-%d")
        except:
            # leave as is if parsing fails
            pass

# Save JSON
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Generate HTML table (optional)
html = "<h2>Gig Graph Data</h2>\n"
html += """
<style>
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background-color: #f2f2f2; }
</style>
"""

if data:
    columns = list(data[0].keys())
    html += "<table><thead><tr>" + "".join(f"<th>{c}</th>" for c in columns) + "</tr></thead><tbody>"
    for row in data:
        html += "<tr>" + "".join(f"<td>{row[c]}</td>" for c in columns) + "</tr>"
    html += "</tbody></table>"
else:
    html += "<p>No data available</p>"

with open("output.html", "w") as f:
    f.write(html)

print("data.json and output.html generated successfully.")
