import json
import dredd_hooks as hooks

# Local stash
stash={}


# Retrieve last backup archive name
@hooks.after('User Backups > List backups > List backups')
def get_last_backup_name(transaction):
            arch_list=json.loads(transaction['real']['body'])
            stash['last_backup_name'] = arch_list[0]['Name']
        
# Set backup arch Name
@hooks.before('User Backups > Restore backup > Restore backup')
def get_last_backup_name(transaction):
            transaction['request']['body'].replace('$BACKUP_ARCHIVE_NAME',stash['last_backup_name'])
		