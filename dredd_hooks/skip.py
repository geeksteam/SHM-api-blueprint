import dredd_hooks as hooks

@hooks.before("Panel Authorization > User login > Login with HOTP success")
def skip_test(transaction):
  transaction['skip'] = True

@hooks.before("Panel Authorization > User login > Login fails because HOTP wrong code")
def skip_test(transaction):
  transaction['skip'] = True

# Skip IMAGE/PNG body
@hooks.beforeValidation("Two step authorization > Generate QR > Getting QR image with code", function (transaction) {
    transaction.real.body = '';
});