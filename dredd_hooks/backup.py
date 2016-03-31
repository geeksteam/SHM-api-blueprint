import json
import dredd_hooks as hooks

# Local stash
last_backup_name = 'noBackup'

# Retrieve last backup archive name
@hooks.after('User Backups > List backups > List backups')
def get_last_backup_name(transaction):
            arch_list=json.loads(transaction['real']['body'])
            print(repr(arch_list))
            last_backup_name = 'noBackupAfter'
        
# Set backup arch Name
@hooks.before('User Backups > Restore backup > Restore backup')
def set_last_backup_name(transaction):
            transaction['request']['headers']['Backup-name'] = last_backup_name
            transaction['request']['body'] = transaction['request']['body'].replace('$BACKUP_ARCHIVE_NAME',last_backup_name)
		