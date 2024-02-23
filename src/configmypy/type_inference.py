# Infer types of argparse arguments intelligently

from argparse import ArgumentTypeError
from typing import Callable


def infer_boolean(var, strict: bool=True):
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
    elif var.lower() == 'None':
        return None
    elif strict:
        raise ArgumentTypeError()
    else:
        return str(var)

def infer_numeric(var, strict: bool=True):
    # int if possible -> float -> NoneType -> Err
    if var.isnumeric():
        return int(var)
    elif '.' in list(var):
        decimal_left_right = var.split('.')
        if len(decimal_left_right) == 2:
            if sum([x.isnumeric() for x in decimal_left_right]) == 2: # True, True otherwise False
                return float(var)
    elif var.lower() == 'none':
        return None
    elif strict:
        raise ArgumentTypeError()
    else:
        return str(var)

def infer_str(var, strict:bool=True):
    """
    infer string values and handle fuzzy None and bool types (optional)

    var: str input
    strict: whether to allow "fuzzy" None types
    """
    if strict:
        return str(var)
    elif var.lower() == 'None':
        return None
    else:
        return str(var)
        

class TypeInferencer(object):
    def __init__(self, orig_type: Callable, strict: bool=True):
        """
        TypeInferencer mediates between argparse
        and ArgparseConfig
        
        orig_type: Callable type
            type of original var from config
        strict: bool, default True
            whether to use type inferencing. If False,
            default to simply applying default type converter.
                This may cause issues for some types:
                ex. if argparseConfig takes a boolean for arg 'x', 
                passing --x False into the command line will return a value
                of True, since argparse works with strings and bool('False') = True.
        strict: bool, default True
            if True, raise ArgumentTypeError when the value cannot be cast to
            the allowed types. Otherwise default to str. 

        """
        self.orig_type = orig_type
        self.strict = strict

    def __call__(self, var):
        """
        Callable method passed to argparse's builtin Callable type argument.
        var: original variable (any type)

        """
        if self.orig_type == bool:
            return infer_boolean(var, self.strict)
        elif self.orig_type == float or self.orig_type == int:
            return infer_numeric(var, self.strict)
        else:
            if self.strict:
                return infer_str(var)
            else:
                return self.orig_type(var)
