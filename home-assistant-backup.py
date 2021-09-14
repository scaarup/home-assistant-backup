#!/usr/bin/env python
# Created by Søren Christian Aarup, sc@aarup.org
# https://github.com/scaarup/home-assistant-backup
# api ref.: https://developers.home-assistant.io/docs/api/supervisor/endpoints

import requests,json,datetime,gzip,sys,datetime
from datetime import timedelta, date
token = 'Bearer <token>'
host = '<url>'
retention = 12 # In days, how many backups do you want to keep on Home Assistant (normally in /backup).
backupname = 'hassio_backup_full-'
date_string = datetime.datetime.now().strftime('%Y%m%d')
_d = date.today() - timedelta(retention)
oldestbackup = backupname+_d.strftime('%Y%m%d')+'.tar.gz'
name = backupname+date_string+'.tar.gz'
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

def listBackups(name):
    debuglog('Looping through backups on HA, looking for '+name)
    response = requests.get(
        host+'/api/hassio/backups',
        headers={'authorization': token}
    )
    json_response = response.json()
    backups = json_response['data']['backups']
    for backup in backups:
        debuglog('\t'+backup['name']+' '+backup['slug'])
        if (backup['name'] == name):
            debuglog('Found our backup on HA:')
            return backup['slug']

def createBackupFull(name):
    debuglog('Creating backup '+name)
    response = requests.post(
        host+'/api/hassio/backups/new/full',
        json={'name': name},
        headers={'authorization': token,'content-type': 'application/json'}
    )
    debuglog(str(response.status_code)+' '+str(response.content))
    json_response = response.json()
    debuglog('Create backup response: '+json_response['result'])
    return json_response['data']['slug']

def removeBackup(name,slug):
    debuglog('Removing backup '+name+' on server')
    response = requests.delete(
        host+'/api/hassio/backups/'+slug,
        headers={'authorization': token,
        'content-type': 'application/json'}
    )
    debuglog(str(response.status_code)+' '+str(response.content))
    json_response = response.json()

def getBackup(name,slug):
    log('Downloading backup '+name)
    response = requests.get(
        host+'/api/hassio/backups/'+slug+'/download',
        headers={'authorization': token}
    )
    output = gzip.open(name, 'wb')
#    try:
    output.write(response.content)
#    finally:
    output.close()
    if response.status_code == 200:
        debuglog('Download ok')
    else:
        debuglog('Download response '+str(response.status_code)+' '+str(response.content))

# Create the backup, get the slug:
slug = createBackupFull(name)
# Download the backup:
getBackup(name,slug)
# Remove our oldest backup, according to retention

slug = listBackups(oldestbackup)
if slug is not None:
    debuglog('Calling removeBackup for '+oldestbackup+' with slug '+slug)
    removeBackup(name,slug)
else:
    debuglog('Did not find a backup to delete.')
