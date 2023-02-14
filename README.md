![PyPI](https://img.shields.io/pypi/v/configmypy)
[![Github Test](https://github.com/JeanKossaifi/configmypy/actions/workflows/test.yml/badge.svg)](https://github.com/JeanKossaifi/configmypy/actions/workflows/test.yml)

# ConfigMyPy

Configure My Python: Easy configuration of Python projects.

## Quickstart

Just clone the repository and install it, here in editable mode:

```bash
git clone https://github.com/JeanKossaifi/configmypy
cd configmypy
python -m pip install -e .
```

Then, assuming you have a configuration file `config.yaml` in your folder, get your configuration using
```python
from configmypy import ConfigPipeline, YamlConfig, ArgparseConfig

pipe = ConfigPipeline([YamlConfig('./config.yaml'),
                        ArgparseConfig()])
config = pipe.read_conf()
```

Then just read your parameters from config:
```
arg = config.arg
arg2 = config['arg2']
...
```

The script will read config.yaml, as well as optional command-line arguments, which will overwrite the config.

## Rationale

How many times did you start having a large Python project, let's say to run some Machine Learning models, where you wanted to change quickly the parameters.
Then you want to track them. In you write a small logger. Then you write a small yaml config file to more easily manage the quickly growing list of parameters.
Then you realize you sometimes need to change some of these parameters on the fly. 
In comes argparse, and you manually override an increasingly long list of paramters with a code becoming a long list of

```python
if args.parameter is not None:
    config['parameter'] = args.parameter
```

...and there goes your sanity... Along with any hope of properly managing and tracking your experiments. 

To address this frustration, I wrote this minimal package that makes this easy.

## Reading from a `.yaml` config file

Imagine you have a `config.yaml` file that looks like this:

```yaml
default:
  opt:
    optimizer: 'adam'
    lr: 0.1
  data:
    dataset: 'ns'
    batch_size: 12
    
test:
  opt:
    optimizer: 'SGD'
```

You can read that using `configmypy.YamlConfig`: 

```yaml
reader = YamlConfig('./config.yaml', config_name='default')
config, _ = reader.read_conf()
```

## Bunch configurations

All our configurations return a Bunch, not a dict. A Bunch is simply a dictionary that exposes its parameters as attributes so you can access them, equivalently, as
`config['param']` or `config.param`.

## Configuration Pipeline

The real power of `configmypy` comes from the ConfigPipeline: you can have several steps called sequentially. 
A typical usecase would be: 
1) Read a default (.yaml) config
2) Optionally overwrite any of those parameters using argparse (command-line arguments)
3) If the user specified another configuration, update the parameters read so far with that new config

This would look like this with `configmypy`:

```python
pipe = ConfigPipeline([YamlConfig('./config.yaml', config_name='default'),
                        ArgparseConfig(config_file=None, config_name=None),
                        YamlConfig()])
config = pipe.read_conf()
```

This will: 
1) first read the `default` section in `config.yaml`
2) update any parameters with those passed by the user, including additional parameters `config_file` and `config_name` which are automatically passed to the next step
3) If the user specified a `config_file`, that will be read by the next step and used to update the configuration.

You can check the configuration by calling `pipe.log()`:

```python
>>> pipe.log()
###############################
#####    CONFIGURATION    #####
###############################

Steps:
------
 (1) YamlConfig with config_file=./config.yaml, config_name=default
 (2) ArgparseConfig with additional config={'config_file': None, 'config_name': None}
 (3) YamlConfig with config_file=config.yaml, config_name=test

-------------------------------

Configuration:
--------------

opt.optimizer=SGD
opt.lr=0.1
data.dataset=ns
data.batch_size=24

###############################

```

## Questions or issues
This is very much a project in development that I wrote for myself and decided to open-source so myself and others could easily reuse it for multiple projects, while knowing it is actually tested!

If you have any questions or find any bugs, please open an issue, or better yet, a pull-request!

