import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def read_google_sheet(sheet_name, worksheet_name, creds_path="creds.json"):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df