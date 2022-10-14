from .bunch import Bunch


def iter_nested_dict_flat(d, separator='.'):
    """Iterate throught the key, items of a nested dict
    keys will be flattened, nesting indicated by the given separator
    
    Parameters
    ----------
    d : dict 
        dictionary to iterate through
    separator : str, default is '.'
        separator to indicate nesting of the keys
    
    Yields
    ------
    nested_key, value
    """
    for key, value in d.items():
        if isinstance(value, dict):
            for nested_key, nested_value in iter_nested_dict_flat(value, separator=separator):
                yield f'{key}{separator}{nested_key}', nested_value
        else:
            yield key, value


def update_nested_dict_from_flat(nested_dict, key, value, separator='.'):
    """Updates inplace a nested dict using a flattened key with nesting represented by a separator
    
    Parameters
    ----------
    nested_dict : dict
    key : str
    value : Object
    separator : str, default is '.'
    """
    keys = key.split(separator, 1)
    if len(keys) == 1:
        nested_dict[keys[0]] = value
    else:
        k, rest = keys
        update_nested_dict_from_flat(nested_dict[k], rest, value, separator=separator)


