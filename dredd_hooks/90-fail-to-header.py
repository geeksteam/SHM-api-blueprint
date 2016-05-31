import dredd_hooks as hooks
        
# Add fail text to header
@hooks.before_each
def add_failtext_to_header(transaction):
            if transaction['skip'] != True:
                    if (transaction['fail'] != True) and (transaction['fail'] != False):
                            transaction['request']['headers']['Dredd-Fail'] = transaction['fail']
