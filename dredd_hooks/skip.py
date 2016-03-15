import dredd_hooks as hooks

# Skip HOTP codes
@hooks.before("Panel Authorization > User login > Login with HOTP success")
def skip_test(transaction):
  transaction['skip'] = True

# Skip HOTP code confirm
@hooks.before("Two step authorization > Check for correct app binding > Code correct")
def skip_test(transaction):
  transaction['skip'] = True

# Skip HOTP QR IMAGE body
@hooks.before_validation("Two step authorization > Generate QR > Getting QR image with code")
def skip_body(transaction):
    transaction['real']['body'] = ''
