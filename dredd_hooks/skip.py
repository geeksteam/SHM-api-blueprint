import dredd_hooks as hooks

@hooks.before("Panel Authorization > User login > Login with HOTP success")
def skip_test(transaction):
  transaction['skip'] = True