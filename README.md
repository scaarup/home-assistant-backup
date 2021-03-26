# home-assistant-backup
This script is meant to run on a server external to where you are running Home Assistant. By design, this script is meant to be run once daily. It will, via the Supervisor API, create a snapshot and download it to where you are running this script. According to configuration it will keep x amount of snapshots on Home Assistant and clean up older ones.

## Configuration
To keep things simple, configuration is done directly inside the script.
### host
This is the url of you Home Assistant. Depending on where you are running this, you can use either the internal or external URL. Check those out in your UI under Configuration -> General
### token
A so called "Long-Lived Access Token" this script will use for authenticating all of the API calls. 
#### Generate a token
In the UI, click on your profile at the bottom left. Scroll all the way down to the bottom and you will see an option to create a token.
### retention
The snapshot which matches retention+1, will be deleted from Home Assistant. Set this to 7 and you will keep the last 7 snapshots on Home Assistant
### snapname
Name naming prefix of the snapshots. Will be reflected in file names and snapshot names.
### debug
Set to 1 to enable debugging.
### Example configuration
```
token = 'Bearer abfe76...'
host = 'http://10.0.0.22:8123'
retention = 10
snapname = 'hassio_snapshot_full-'
```
## How to run/schedule this
You could schedule this script in crontab like this:

```0 1 * * * cd /mnt/usb/backup;./backup.py```

