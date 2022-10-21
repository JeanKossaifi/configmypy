from ruamel.yaml import YAML
from .bunch import Bunch
from pathlib import Path

class YamlConfig:
    """Read a yaml config file and export it as a dict
    
    Parameters
    ----------
    config_file : str, default is None
    config_name : str, default is None
    """
    def __init__(self, config_file=None, config_name=None, config_folder='.'):
        self.config_file = config_file
        self.config_name = config_name
        self.config_folder = config_folder
    
    def read_conf(self, config=None, config_file=None, config_name=None, config_folder=None):
        """Actually read the conf from the specified yaml file

        .. important::
        
            Please note that values passed in the __init__ take precedence!
            If a config is passed, that given config (assumed to be a dict) will be updated 
            with the new values
        
        Parameters
        ----------
        config : dict, default is None
            if not None, a dict config to update
        config_file : str, default is None
        config_name : str, default is None
        
        Returns
        -------
        Bunch : dict-like
            the read config
        {} : empty dict
            Nothing to be passed to the next config
        """
        # Values passed here take precedence
        # However, if none give, use the old ones
        if config_file is not None:
            self.config_file = config_file
        else:
            config_file = self.config_file

        if config_name is not None:
            self.config_name = config_name
        else:
            config_name = self.config_name
        
        if config_folder is not None:
            self.config_folder = config_folder
        else:
            config_folder = self.config_folder
    
        # Nothing to read
        if config_file is None:
            return config, {}

        filepath = Path(config_folder).resolve().joinpath(config_file).as_posix()
        self.filepath = filepath
        # Read the conf
        yaml=YAML()
        with open(filepath, 'r') as f:
            self.config = yaml.load(f)
        
        if config_name is not None:
            self.config = self.config[config_name]
        
        # IMPORTANT: only work with Bunch otherwise nested updates will be messed up
        self.config = Bunch(self.config)
        
        if config is not None:
            config = Bunch(config)
            config.update(self.config)
        else:
            config = self.config

        return config, {}

    def __str__(self):
        return f'{self.__class__.__name__} with config_file={self.config_file}, config_name={self.config_name}, config_folder={self.config_folder}'
