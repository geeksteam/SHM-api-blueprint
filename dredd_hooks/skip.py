import dredd_hooks as hooks

# Skip HOTP codes
@hooks.before("Panel Authorization > User login > Login with HOTP success")
def skip_test(transaction):
  transaction['skip'] = True

# Skip IMAGE/PNG body
@hooks.before_validation("Two step authorization > Generate QR > Getting QR image with code")
def skip_body(transaction):
    transaction['real']['body'] = ''
