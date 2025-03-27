import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import os

def read_google_sheet(sheet_name, worksheet_name, creds_path="creds.json"):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(os.environ[GOOGLE_CREDS])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df