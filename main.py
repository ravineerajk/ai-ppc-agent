from read_sheet import read_google_sheet

# Replace with your actual sheet and tab names
sheet_name = "CampaignReport"
worksheet_name = "Sheet1"

df = read_google_sheet(sheet_name, worksheet_name)
print(df.head())