# PekoSodies Spreadsheet Exporter and Uploader Script

## General Setup
First, install Python 3.X and the required libraries through `pip install -r requirements.txt`.

## Config
The config is designed to be as user friendly as possible, allowing for everything to be configurable.

First, rename the `example_config.yml` file to `config.yml`.

```yml
General:
    FILE_NAME: ""
```
This is the file name of the file. This name will be displayed in dropbox. You must keep the same filename here as in `DROPBOX_FILE_PATH`.

```yml
Google:
    GOOGLE_CLIENT_SECRET_FILE_NAME: ""
```
Google requires a client secret FILE. This is the name of that file (filepath). To retrieve this, you need to go to https://console.cloud.google.com/welcome?organizationId=0. From here, click the dropdown towards the top left of your screen and choose "New Project" in the top right. Feel free to name this whatever you want. After it is created, make sure it is selected on the top left of your screen and choose "APIs & Services". Click on "ENABLE APIS AND SERVICES". Search for "Google Drive API", click on it, and enable it. You will also need to search for "Google Sheets API" and enable it. Now, you can go back to the Project Details and click on "Credentials". From here, click on "Manage service accounts" and in the top middle of your screen, choose "CREATE SERVICE ACCOUNT". You can name this account anything you want, I recommend to same name as your project. The ID will automatically generate, I do not recommend touching that. You can give it a description if you want, it is not required. Next, click continue twice until you're on "Grant users access to this service account" where you will add your gmail account on both of those boxes. Now you can finally create the account. Once it has been created, select it and choose "Keys". Click "ADD KEY" and "Create new key". Make sure JSON is select and "CREATE". It should automatically download the file where you can put it within this script's folder. Next, update the "GOOGLE_CLIENT_SECRET_FILE_NAME" in your config with the filename.

```yml
Google:
    GOOGLE_SPREADSHEET_ID: ""
```
This step is much more simple. You need to simply get the ID to your spreadsheet which is found in the URL of that spreadsheet. Example URL: `https://docs.google.com/spreadsheets/d/1KU8TXn5QYtZnQxEBIzI41QygNKrehviEoBbmQ8dOFIs/edit#gid=0` Example ID: `1KU8TXn5QYtZnQxEBIzI41QygNKrehviEoBbmQ8dOFIs`.

```yml
Dropbox:
    DROPBOX_ACCESS_TOKEN: ""
```
Just like Google, Dropbox requires an access token as well. You can go to this link: https://www.dropbox.com/developers/apps/ and "Create app". Click "Scoped access" and "Full Dropbox". You can name this app anything you want and "Create app". After it's created, click on "Permissions" and select everything EXCEPT OpenID Scopes. After all permissions are selected, go to "Settings" and "Generate access token". Lastly, simply update the "DROPBOX_ACCESS_TOKEN" in your config.

```yml
Dropbox:
    DROPBOX_FILE_PATH: ""
```
This is where you will input the path where you want the file to be uploaded in. You can leave it as just the txt file or you can specify a specific path. `/path/to/your_file_name.txt` is an example of a specific path and `your_file_name.txt` is an example of leaving it as the txt file. This will automatically create the folders necessary for the path.
