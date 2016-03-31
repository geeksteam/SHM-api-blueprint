import json
import dredd_hooks as hooks

# Local stash
response_stash = {}
last_backup_name = 'noBackup'

# Retrieve last backup archive name
@hooks.after('User Backups > List backups > List backups')
def save_last_backup_name(transaction):
            response_stash[transaction['name']] = transaction['real']
        
# Set backup arch Name
@hooks.before('User Backups > Restore backup > Restore backup')
def set_last_backup_name(transaction):
            
            # parsed_body = json.loads(response_stash['User Backups > List backups > List backups'])
            # last_backup_name = parsed_body[1]['Name']
            
            transaction['request']['headers']['Backup-name'] = last_backup_name
            transaction['request']['body'] = transaction['request']['body'].replace('$BACKUP_ARCHIVE_NAME',last_backup_name)
		