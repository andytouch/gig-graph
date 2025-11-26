import gspread
import pandas as pd
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials from GitHub secret
creds_json = os.environ["GOOGLE_CREDENTIALS"]
sheet_id = os.environ["SHEET_ID"]

# Write credentials to file
with open("creds.json", "w") as f:
    f.write(creds_json)

scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
gc = gspread.authorize(creds)

sheet = gc.open_by_key(sheet_id).sheet1
data = sheet.get_all_records()

# Save raw data
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Example: generate HTML snippet
html = "<h2>Gig Graph Data</h2><ul>"
for row in data:
    html += f"<li>{row}</li>"
html += "</ul>"

with open("output.html", "w") as f:
    f.write(html)
