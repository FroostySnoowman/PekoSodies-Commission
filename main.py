import webbrowser
import requests
import dropbox
import asyncio
import pathlib
import base64
import yaml
import json
from datetime import datetime, timedelta
from ruamel.yaml import YAML
from gsheets import Sheets

# Function to load configuration from the YAML file
def load_config():
    with open(f'{pathlib.Path(__file__).parent.absolute()}/config.yml', 'r') as file:
        data = yaml.safe_load(file)
    return data

config = load_config()

async def export_spreadsheet():
    sheets = Sheets.from_files(f'{pathlib.Path(__file__).parent.absolute()}/{config["Google"]["GOOGLE_CLIENT_SECRET_FILE_NAME"]}')
    spreadsheet = sheets[config["Google"]["GOOGLE_SPREADSHEET_ID"]]
    sheet = spreadsheet.sheets[0]
    df = sheet.to_frame()
    df.to_csv(f'{pathlib.Path(__file__).parent.absolute()}/{config["General"]["FILE_NAME"]}', sep='\t', index=False)

async def upload_txt():
    dbx_token = config["Dropbox"]["DROPBOX_ACCESS_TOKEN"]
    dbx = dropbox.Dropbox(dbx_token)
    with open(f'{pathlib.Path(__file__).parent.absolute()}/{config["General"]["FILE_NAME"]}', "rb") as f:
        dbx.files_upload(f.read(), config["Dropbox"]["DROPBOX_FILE_PATH"], mode=dropbox.files.WriteMode('overwrite'))
    print(f"Successfully uploaded the file to Dropbox at {datetime.now()}")

async def main():
    await export_spreadsheet()
    await upload_txt()

async def run_every_hour():
    global config
    try:
        await main()
        while True:
            now = datetime.now()
            next_run = now + timedelta(hours=1)
            next_run = next_run.replace(minute=now.minute, second=0, microsecond=0)
            seconds_until_next_run = (next_run - now).total_seconds()
            await asyncio.sleep(seconds_until_next_run)
            await main()
    except dropbox.exceptions.AuthError:
        url = f'https://www.dropbox.com/oauth2/authorize?client_id={config["Dropbox"]["APP_KEY"]}&' \
            f'response_type=code&token_access_type=offline'
        webbrowser.open(url)

        access_code_generated = input("Enter access token: ")

        basic_auth = base64.b64encode(f'{config["Dropbox"]["APP_KEY"]}:{config["Dropbox"]["APP_SECRET"]}'.encode()).decode()

        headers = {
            'Authorization': f"Basic {basic_auth}",
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = f'code={access_code_generated}&grant_type=authorization_code'

        response = requests.post('https://api.dropboxapi.com/oauth2/token',
                                data=data,
                                headers=headers)

        new_access_token = json.loads(response.text)['access_token']

        new_yaml = YAML()
        new_yaml.preserve_quotes = True
        new_yaml.indent(mapping=4, sequence=4, offset=2)
        with open(f'{pathlib.Path(__file__).parent.absolute()}/config.yml', 'r') as file:
            new_data = new_yaml.load(file)
        new_data['Dropbox']['DROPBOX_ACCESS_TOKEN'] = new_access_token

        with open(f'{pathlib.Path(__file__).parent.absolute()}/config.yml', 'w') as file:
            new_yaml.dump(new_data, file)
        
        config = load_config()

        await main()

if __name__ == "__main__":
    print("Script has started running!")
    asyncio.run(run_every_hour())

if __name__ == "__main__":
    print("Script has started running!")
    asyncio.run(run_every_hour())