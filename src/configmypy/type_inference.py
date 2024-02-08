# Infer types of argparse arguments intelligently

from argparse import ArgumentTypeError


def infer_boolean(var):
    if var.lower() == 'true':
        return True
    elif var.lower() == 'false':
        return False
    else:
        raise ArgumentTypeError()

def infer_numeric(var):
    # infer float
    if '.' in list(var):
        return float(var)
    elif var.isnumeric():
        return int(var)
    else:
        raise ArgumentTypeError()

