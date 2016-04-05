import dredd_hooks as hooks

#
# Run only current GROUP of tests instead of all, empty will run all tests.
run_only_groups = [
        'Panel Authorization',
        'Exim Logs',
        'DNSBL spam lists',
        'System Services',
        'System Processes',
        'Open SSH server',
        'Fail2ban',
        'Logout',
     ]
#
# List certain of GROUPS to skip
skip_groups = []

#
# List certain of REQUESTS to skip
skip_requests = [
		'Panel Authorization > User login > Login with HOTP success',
		'Two step authorization > Check for correct app binding > HOTP app Code correct',
		'File uploads > Upload file in temporary storage > Upload file',
		'MySQL Databases > Export database > Export database',
		'PgSQL Databases > Export database > Export database',
        'Filemanager > Download files > Download file',
        'Filemanager > Download files > Download file by #User',
	]

# Skip all except Run ONLY GROUP
@hooks.before_each
def skip_run_only_func(transaction):
        if len(run_only_groups) > 0:
                # Check is request GROUP in SKIP list
                if transaction['origin']['resourceGroupName'] not in run_only_groups:
                        transaction['skip'] = True

# Skip requests and groups
@hooks.before_each
def skip_requests_func(transaction):
        # Check is request GROUP in SKIP list
        if transaction['origin']['resourceGroupName'] in skip_groups:
		        transaction['skip'] = True
        # Check for request
        if transaction['name'] in skip_requests:
		        transaction['skip'] = True

#
# Skip HOTP QR IMAGE body
@hooks.before_validation("Two step authorization > Generate QR > Getting QR image with code")
def skip_hotp_image(transaction):
        if transaction['skip'] != True:
                transaction['real']['body'] = ''
