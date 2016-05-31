import json
import sys
import dredd_hooks as hooks

# Local stash
last_backup_name = 'noBackupFound'

# Retrieve last backup archive name
@hooks.after('User Backups > List backups > List backups')
def save_last_backup_name(transaction):
            if transaction['skip'] != True:
                    global last_backup_name
                    response_json = json.loads(transaction['real']['body'])
                    if len(response_json) > 0:
                            last_backup_name = response_json[0]['Name']
        
# Set backup arch Name
@hooks.before('User Backups > Restore backup > Restore backup')
def set_last_backup_restore_name(transaction):
            if transaction['skip'] != True:
                    transaction['request']['headers']['Backup-name'] = last_backup_name
                    transaction['request']['body'] = transaction['request']['body'].replace('$BACKUP_NAME',last_backup_name)

# Set backup arch Name
@hooks.before('User Backups > Delete backup > Delete backup')
def set_last_backup_delte_name(transaction):
            if transaction['skip'] != True:
                    transaction['request']['headers']['Backup-name'] = last_backup_name
                    transaction['request']['body'] = transaction['request']['body'].replace('$BACKUP_NAME',last_backup_name)
