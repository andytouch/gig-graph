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

# Authorize and fetch sheet
scope = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(sheet_id).sheet1
data = sheet.get_all_records()

# Calculate totals
total_concerts = len(data)
unique_artists = len(set(row.get('Artist', '').strip() for row in data if row.get('Artist', '').strip()))

# Generate JSON with both raw data and summary
output = {
    "summary": {
        "total_concerts": total_concerts,
        "total_musicians": unique_artists
    },
    "rows": data
}

with open("data.json", "w") as f:
    json.dump(output, f, indent=2)

print("data.json generated with summary and rows")
