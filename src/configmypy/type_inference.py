# Infer types of argparse arguments intelligently

from argparse import ArgumentTypeError
from typing import Callable


def infer_boolean(var):
    """
    accept argparse inputs of string, correctly
    convert into bools. Without this behavior, 
    bool('False') becomes True by default.

    Parameters
    ----------
    var: input from parser.args
    """
    if var.lower() == 'true':
        return True
    elif var.lower() == 'false':
        return False
    else:
        raise ArgumentTypeError()

def infer_numeric(var):
    # infer numeric values using simple hierarchy
    # int if possible -> float -> NoneType
    if '.' in list(var):
        return float(var)
    elif var.isnumeric():
        return int(var)
    elif var.lower() == 'none' or var.lower() == 'false':
        return None
    else:
        raise ArgumentTypeError()


class TypeInferencer(object):
    def __init__(self, orig_type: Callable, strict: bool=False):
        """
        TypeInferencer mediates between argparse
        and ArgparseConfig
        
        """
        self.orig_type = orig_type
        self.strict = strict

    def __call__(self, var):
        if self.strict:
            return self.orig_type(var)
        else:
            if orig_type == bool:
                return infer_boolean(var)
            elif orig_type == float or orig_type == int:
                return infer_numeric(var)
            else:
                # add infer_list, etc?
                return self.orig_type(var)




