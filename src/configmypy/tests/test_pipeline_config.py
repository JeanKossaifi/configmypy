from ..bunch import Bunch
from ..yaml_config import YamlConfig
from ..argparse_config import ArgparseConfig
from ..pipeline_config import ConfigPipeline


TEST_CONFIG_FILE = """\
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
"""

TEST_CONFIG_DICT = {
  'default': {'opt': {'optimizer': 'adam', 'lr': 0.1},
              'data': {'dataset': 'ns', 'batch_size': 12}},
  'test': {'opt': {'optimizer': 'SGD'}}
}


def test_ConfigPipeline(mocker, monkeypatch):
    """"Test for ConfigPipeline"""
    mocker.patch("builtins.open", mocker.mock_open(read_data=TEST_CONFIG_FILE))
    monkeypatch.setattr("sys.argv", ['test', '--data.batch_size', '24', '--config_file', 'config.yaml', '--config_name', 'test'])

    true_config = Bunch(TEST_CONFIG_DICT['default'])
    true_config.data.batch_size = 24
    true_config.opt.optimizer = 'SGD'

    pipe = ConfigPipeline([
                            YamlConfig('./config.yaml', config_name='default'),
                            ArgparseConfig(config_file=None, config_name=None),
                            YamlConfig()
                            ])
    config = pipe.read_conf()
    
    assert config == true_config
