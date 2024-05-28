import argparse
from copy import deepcopy
from ctypes import ArgumentError
from .bunch import Bunch
from .utils import iter_nested_dict_flat
from .utils import update_nested_dict_from_flat
from .type_inference import TypeInferencer

class ArgparseConfig:
    """Read config from the command-line using argparse
    
    We take in a configuration dictionary and use it to populate the argparse Namespace. 
    
    Parameters
    ----------
    infer_types : False or literal['fuzzy', 'strict']
        if False, use python's typecasting from type(value) to indicate expected type
        if fuzzy, use custom type handling and allow all types to take values of None
        if strict, use custom type handling but do not allow passing bool or None to other types.

    overwrite_nested_config : bool, default is True
        if True, users can set values at different levels of nesting
        e.g. if you have a field::

            mlp:
              in_features: 64
              out_features: 128

        then users could set `mlp.in_features` or disable mlp alltogether by
        setting `mlp=None`

    **additional_config : dict
        key, values to read from command-line and pass on to the next config
    """
    def __init__(self, infer_types="fuzzy", overwrite_nested_config=False, **additional_config):
        self.additional_config = Bunch(additional_config)
        if infer_types in [False, "fuzzy", "strict"]:
            self.infer_types = infer_types
        elif infer_types:
            # Backwards compatibility
            self.infer_types = 'strict'
        else:
            raise ArgumentError("Error: infer_types only takes values False, \'fuzzy\', \'strict\'")
        self.overwrite_nested_config = overwrite_nested_config
    
    def read_conf(self, config=None, **additional_config):
        """
        Please note that values passed in the __init__ take precedence!
        If a config is passed, that given config (assumed to be a dict) will be updated 
        with the new values
        
        Parameters
        ----------
        config : dict, default is None
            if not None, a dict config to update
        infer_types: bool, default is False
            if True, uses custom type handling
            where all values, regardless of type,
            may take the value None. 
            If false, uses default argparse
            typecasting
        additional_config : dict
        
        Returns
        -------
        Bunch : dict-like
            the read config
        Bunch : empty dict
            additional_config to be passed to the next config
        """
        config = Bunch(config)
        additional_config = Bunch(additional_config)
        
        additional_config.update(self.additional_config)
        config.update(self.additional_config)
        
        parser = argparse.ArgumentParser(description='Read the config from the commandline.')
        for key, value in iter_nested_dict_flat(config, return_intermediate_keys=self.overwrite_nested_config):
                # smartly infer types if infer_types is turned on 
                # otherwise force default typecasting
                if self.infer_types:
                    if self.infer_types == 'strict':
                        strict=True
                    elif  self.infer_types == 'fuzzy':
                        strict=False
                    type_inferencer = TypeInferencer(orig_type=type(value), strict=strict)
                else:
                    type_inferencer = type(value)

                parser.add_argument(f'--{key}', type=type_inferencer, default=value)

        args = parser.parse_args()
        self.config = Bunch(args.__dict__)        

        if config is not None:
            config = Bunch(config)
            if self.overwrite_nested_config:
                # Create a copy
                trimmed_config = Bunch(self.config)

                # Remove subdict if overwritten by users
                for key, value in self.config.items():
                    if value is None or not value:
                        for subkey in self.config.keys():
                            if subkey.startswith(key) and (key != subkey):
                                print('removing subdict', subkey)
                                trimmed_config.pop(subkey)
                    elif key in trimmed_config:
                        # Value is True: delete the key if it has leafs
                        for subkey in self.config.keys():
                            if subkey.startswith(key) and (key != subkey):
                                print('removing root', key)
                                print(subkey.startswith(key), subkey, key)
                                trimmed_config.pop(key)
                                break
                self.config = trimmed_config

            # Update the config passed by the user with the new one
            for key, value in self.config.items():
                update_nested_dict_from_flat(config, key, value)
        else:
            config = self.config
        
        kwargs = {k: config.pop(k) for k in additional_config}

        return config, kwargs

    def __str__(self):
        return f'{self.__class__.__name__} with additional config={self.additional_config}'
        
