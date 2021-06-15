#!/usr/bin/env python
# Created by Søren Christian Aarup, sc@aarup.org
# https://github.com/scaarup/home-assistant-backup
# api ref.: https://developers.home-assistant.io/docs/api/supervisor/endpoints
import requests,json,datetime,gzip,sys,datetime
from datetime import timedelta, date
token = 'Bearer X'
host = 'https://<ha-hostname>'
retention = 12 # In days, how many snapshots do you want to keep on Home Assistant (normally in /backup).
snapname = 'hassio_snapshot_full-'
date_string = datetime.datetime.now().strftime('%Y%m%d')
_d = date.today() - timedelta(retention)
oldestsnap = snapname+_d.strftime('%Y%m%d')+'.tar.gz'
name = snapname+date_string+'.tar.gz'
debug = 1

def debuglog(msg):
    if debug == 1:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' DEBUG: '+msg)
def log(msg):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' INFO: '+msg)

# Ping Supervisor, quit if fail:
response = requests.get(host+'/api/hassio/supervisor/ping', headers={'authorization': token})
json_response = response.json()
if not json_response['result'] == 'ok':
    log('Supervisor not responding ok to our ping! '+str(response.status_code)+' '+str(response.content))
    sys.exit(1)
##

def listSnapshots(name):
    debuglog('Looping through snapshots on HA, looking for '+name)
    response = requests.get(
        host+'/api/hassio/snapshots',
        headers={'authorization': token}
    )
    json_response = response.json()
    snapshots = json_response['data']['snapshots']
    for snapshot in snapshots:
        debuglog('\t'+snapshot['name']+' '+snapshot['slug'])
        if (snapshot['name'] == name):
            debuglog('Found our snapshot on HA:')
            return snapshot['slug']

def createSnapshotFull(name):
    debuglog('Creating snapshot '+name)
    response = requests.post(
        host+'/api/hassio/snapshots/new/full',
        json={'name': name},
        headers={'authorization': token,'content-type': 'application/json'}
    )
    debuglog(str(response.status_code)+' '+str(response.content))
    json_response = response.json()
    debuglog('Create snapshot response: '+json_response['result'])
    return json_response['data']['slug']

def removeSnapshot(name,slug):
    debuglog('Removing snapshot '+name+' on server')
    response = requests.delete(
        host+'/api/hassio/snapshots/'+slug,
        headers={'authorization': token,
        'content-type': 'application/json'}
    )
    debuglog(str(response.status_code)+' '+str(response.content))
    json_response = response.json()

def getSnapshot(name,slug):
    log('Downloading snapshot '+name)
    response = requests.get(
        host+'/api/hassio/snapshots/'+slug+'/download',
        headers={'authorization': token}
    )
    output = gzip.open(name, 'wb')
    output.write(response.content)
    output.close()
    if response.status_code == 200:
        debuglog('Download ok')
    else:
        debuglog('Download response '+str(response.status_code)+' '+str(response.content))

# Create the snapshot, get the slug:
slug = createSnapshotFull(name)
# Download the snapshot:
getSnapshot(name,slug)
# Remove our oldest snapshot, according to retention

slug = listSnapshots(oldestsnap)
if slug is not None:
    debuglog('Calling removeSnapshot for '+oldestsnap+' with slug '+slug)
    removeSnapshot(name,slug)
else:
    debuglog('Did not find a snapshot to delete.')
