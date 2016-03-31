import json
import dredd_hooks as hooks

# Local stash
response_stash = {}
last_backup_name = 'noBackup'

def save_response_to_stash(transaction):
            # saving HTTP response to the stash
            response_stash[transaction['name']] = transaction['real']

# Retrieve last backup archive name
@hooks.after('User Backups > List backups > [120] ( Timer:10) List backups')
def get_last_backup_name(transaction):
            save_response_to_stash(transaction)
            blablabla
        
# Set backup arch Name
@hooks.before('User Backups > Restore backup > Restore backup')
def set_last_backup_name(transaction):
            transaction['request']['headers']['Backup-name'] = last_backup_name
            transaction['request']['body'] = transaction['request']['body'].replace('$BACKUP_ARCHIVE_NAME',last_backup_name)
		