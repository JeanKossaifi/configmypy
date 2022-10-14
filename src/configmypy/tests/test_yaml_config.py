from ..yaml_config import YamlConfig
from ..bunch import Bunch


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

def test_YamlConfig(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data=TEST_CONFIG_FILE))

    reader = YamlConfig('./config.yaml', config_name='default')
    config, _ = reader.read_conf()
    true_config = Bunch(TEST_CONFIG_DICT['default'])
    assert config == true_config
    
    reader = YamlConfig('./config.yaml', 'test')
    new_config, _ = reader.read_conf(config)
    true_config.opt.optimizer = 'SGD'
    assert new_config == true_config
