# Infer types of argparse arguments intelligently

from argparse import ArgumentTypeError
from ast import literal_eval
from typing import Callable

# import custom Yaml types to handle sequences
from ruamel.yaml import CommentedSeq, CommentedMap


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

def infer_iterable(var, inner_type: Callable=None, strict: bool=True):
    # Use ast.literal_eval to parse the iterable tree,
    # then use custom type handling to infer the inner types
    raw_ast_iter = literal_eval(var)
    if inner_type is not None:
        return iterable_helper(raw_ast_iter, inner_type, strict)
    else:
        # currently argparse config cannot support inferring
        # more granular types than list or tuple
        return raw_ast_iter
    

def iterable_helper(var, inner_type: Callable, strict: bool=True):
    """
    recursively loop through iterable and apply custom type
    callables to each inner variable to conform to strictness
    """
    if isinstance(var, list):
        return [iterable_helper(x,inner_type, strict) for x in var]
    elif isinstance(var, tuple):
        return tuple([iterable_helper(x,inner_type, strict) for x in var])
    else:
        return inner_type(str(var),strict)
    

class TypeInferencer(object):
    def __init__(self, orig_type: Callable, strict: bool=True):
        """
        TypeInferencer mediates between argparse
        and ArgparseConfig
        
        orig_type: Callable type
            type of original var from config
            cannot be NoneType - defaults to infer_str
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
        if orig_type == type(None):
            self.orig_type = infer_str
        else:
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
        elif self.orig_type == tuple or self.orig_type == list or self.orig_type == CommentedMap or self.orig_type == CommentedSeq:
            return infer_iterable(var, None, self.strict)
        else:
            if self.strict:
                return infer_str(var)
            else:
                return self.orig_type(var)
