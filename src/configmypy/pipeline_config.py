from .utils import iter_nested_dict_flat

class ConfigPipeline:
    """Read configuration from a variety of places and compose them
    
    This class aims to simplifying the configuration of Python project.
    A typical usecase is to have a yaml default config, which can be 
    automatically overwritten via the command-line.
    
    Optionally, the command-line also lets you read yet another config. 
    """
    def __init__(self, steps):
        self.steps = steps
    
    def read_conf(self):
        config = None
        kwargs = dict()
        for step in self.steps:
            config, kwargs = step.read_conf(config, **kwargs)
        
        self.config = config

        return config
    
    def log(self):
        print('###############################')
        print('#####    CONFIGURATION    #####')
        print('###############################')
        print('\nSteps:')
        print('------')
        for i, step in enumerate(self.steps):
            print(f' ({i+1}) {step}')
        print('\n-------------------------------')
        print('\nConfiguration:')
        print('--------------\n')
        for key, value in iter_nested_dict_flat(self.config):
            print(f'{key}={value}')
        print('\n###############################')

