import dredd_hooks as hooks

@hooks.before_each
def remove_trailing_newline(transaction):
  if transaction['expected']['headers']['Content-Type'] == 'text/plain':
    transaction['expected']['body'] = transaction['expected']['body'].rstrip()
