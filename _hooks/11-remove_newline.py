import dredd_hooks as hooks

# Removing new line bug
@hooks.before_each
def remove_trailing_newline(transaction):
        if  'headers' in transaction['expected'] and 'Content-Type' in transaction['expected']['headers']:
                if 'text/plain' in transaction['expected']['headers']['Content-Type']:
                        transaction['expected']['body'] = transaction['expected']['body'].rstrip()
