import argparse
from .bunch import Bunch
from .utils import iter_nested_dict_flat
from .utils import update_nested_dict_from_flat


class ArgparseConfig:
    """Read config from the command-line using argparse
    
    We take in a configuration dictionary and use it to populate the argparse Namespace. 
    
    Parameters
    ----------
    infer_types : bool, default is True
        if True, use type(value) to indicate expected type
    **additional_config : dict
        key, values to read from command-line and pass on to the next config
    """
    def __init__(self, infer_types=True, **additional_config):
        self.additional_config = Bunch(additional_config)
        self.infer_types = infer_types
    
    def read_conf(self, config=None, **additional_config):
        """
        Please note that values passed in the __init__ take precedence!
        If a config is passed, that given config (assumed to be a dict) will be updated 
        with the new values
        
        Parameters
        ----------
        config : dict, default is None
            if not None, a dict config to update
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
        for key, value in iter_nested_dict_flat(config):
            if self.infer_types and value is not None:
                parser.add_argument(f'--{key}', type=type(value), default=value)
            else:
                parser.add_argument(f'--{key}', default=value)

        args = parser.parse_args()
        self.config = Bunch(args.__dict__)        

        if config is not None:
            config = Bunch(config)
            for key, value in self.config.items():
                update_nested_dict_from_flat(config, key, value)
        else:
            config = self.config
        
        kwargs = {k: config.pop(k) for k in additional_config}

        return config, kwargs

    def __str__(self):
        return f'{self.__class__.__name__} with additional config={self.additional_config}'
        
