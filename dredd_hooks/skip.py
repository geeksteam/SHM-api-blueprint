import dredd_hooks as hooks

#
# List of requests NAMEs to skip
skip_requests = [
		'Panel Authorization > User login > Login with HOTP success',
		'Two step authorization > Check for correct app binding > HOTP app Code correct',
		#'File uploads > Upload file in temporary storage > Upload file',
	]


# Skip requests
@hooks.before_each
def skip_requests_func(transaction):
	if transaction['name'] in skip_requests:
		transaction['skip'] = True

#
# Skip HOTP QR IMAGE body
@hooks.before_validation("Two step authorization > Generate QR > Getting QR image with code")
def skip_hotp_image(transaction):
    transaction['real']['body'] = ''
