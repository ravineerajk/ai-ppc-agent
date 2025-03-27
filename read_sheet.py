import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def read_google_sheet(sheet_name, worksheet_name):
    # Use Streamlit secrets (this works locally and on Streamlit Cloud)
    from streamlit import secrets

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # Load from Streamlit secrets (as JSON string)
    creds_dict = json.loads(secrets["GOOGLE_CREDS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(worksheet_name)

    data = sheet.get_all_records()
    return pd.DataFrame(data)