# home-assistant-backup
This script is meant to run on a server external to where you are running Home Assistant. By design, this script is meant to be run once daily. It will, via the Supervisor API, create a backup and download it to where you are running this script. According to configuration it will keep x amount of backups on Home Assistant and clean up older ones.

## Installation
Hop on your Linux og Mac (havn't tried on Windows).
1. ```$ git clone https://github.com/scaarup/home-assistant-backup```
2. ```$ cd home-assistant-backup```
3. ```$ pip install -r requirements.txt```

## Configuration
To keep things simple, configuration is done directly inside the script. The example below is pretty self explanatory, but each parameter is documented as well.
### Example configuration
```
token = 'Bearer abfe76...'
host = 'http://10.0.0.22:8123'
retention = 10
backupname = 'hassio_backup_full-'
debug = 1
```
### host
This is the url of you Home Assistant. Depending on where you are running this, you can use either the internal or external URL. Check those out in your UI under Configuration -> General
### token
A so called "Long-Lived Access Token" this script will use for authenticating all of the API calls. 
#### Generate a token
In the UI, click on your profile at the bottom left. Scroll all the way down to the bottom and you will see an option to create a token.
### retention
The backup which matches retention+1, will be deleted from Home Assistant. Set this to 7 and you will keep the last 7 backups on Home Assistant
### backupname
Name naming prefix of the backupss. Will be reflected in file names and backup names.
### debug
Set to 1 to enable debugging.

## How to run/schedule this
You could schedule this script in crontab like this:

```0 1 * * * cd /mnt/usb/backup;./home-assistant-backup.py```

