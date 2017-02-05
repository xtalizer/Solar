#Charge controller

def control(pow_mod,pow_load):
    '''
    returns power into or out from battery
    sign convention: + is in; - is out
    '''
    return -pow_load-pow_mod