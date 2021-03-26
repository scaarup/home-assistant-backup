# home-assistant-backup
This script is meant to run on a server external to where you are running Home Assistant. It will, via the Supervisor API, create a snapshot and download it to where you are running this script. According to configuration it will keep x amount of snapshots on Home Assistant and clean up older ones.

## Configuration
To keep things simple, configuration is done directly inside the script.
### host
This is the url of you Home Assistant. Depending on where you are running this, you can use either the internal or external URL. Check those out in your UI under Configuration -> General
### token
A so called "Long-Lived Access Token" this script will use for authenticating all of the API calls. 
#### Generate a token
In the UI, click on your profile at the bottom left. Scroll all the way down to the bottom and you will see an option to create a token.

## How to run/schedule this
You could schedule this script in crontab like this:

```0 1 * * * cd /mnt/usb/backup;./backup.py```

