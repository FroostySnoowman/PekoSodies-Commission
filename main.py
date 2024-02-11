import dropbox
import asyncio
import yaml
from datetime import datetime, timedelta
from gsheets import Sheets

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

file_name = data["General"]["FILE_NAME"]
google_client_secret_file_name = data["Google"]["GOOGLE_CLIENT_SECRET_FILE_NAME"]
google_spreadsheet_id = data["Google"]["GOOGLE_SPREADSHEET_ID"]
dropbox_acces_token = data["Dropbox"]["DROPBOX_ACCESS_TOKEN"]
dropbox_file_path = data["Dropbox"]["DROPBOX_FILE_PATH"]

async def export_spreadsheet():
    sheets = Sheets.from_files(google_client_secret_file_name)

    spreadsheet = sheets[google_spreadsheet_id]

    sheet = spreadsheet.sheets[0]

    df = sheet.to_frame()

    df.to_csv(file_name, sep='\t', index=False)

async def upload_txt():
    dbx_token = dropbox_acces_token
    dbx = dropbox.Dropbox(dbx_token)

    with open(file_name, "rb") as f:
        dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode('overwrite'))
    
    print(f"Successfully uploaded the file to Dropbox at {datetime.now()}")

async def main():
    await export_spreadsheet()
    await upload_txt()

async def run_at_top_of_hour():
    while True:
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        seconds_until_next_hour = (next_hour - now).total_seconds()
        await asyncio.sleep(seconds_until_next_hour)
        await main()

if __name__ == "__main__":
    print("Script has started running!")
    asyncio.run(run_at_top_of_hour())