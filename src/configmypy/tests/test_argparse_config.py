from ..argparse_config import ArgparseConfig
from ..bunch import Bunch


TEST_CONFIG_DICT = {
  'default': {'opt': {'optimizer': 'adam', 'lr': 0.1},
              'data': {'dataset': 'ns', 'batch_size': 12}},
  'test': {'opt': {'optimizer': 'SGD'}}
}


def test_ArgparseConfig(monkeypatch):
    monkeypatch.setattr("sys.argv", ['test', '--data.batch_size', '24'])
    config = Bunch(TEST_CONFIG_DICT['default'])
    parser = ArgparseConfig(infer_types=True)
    args, kwargs = parser.read_conf(config)
    config.data.batch_size = 24
    assert config == args
    assert kwargs == {}

    monkeypatch.setattr("sys.argv", ['test', '--data.batch_size', '24', '--config_name', 'test'])
    config = Bunch(TEST_CONFIG_DICT['default'])
    parser = ArgparseConfig(infer_types=True, config_name=None)
    args, kwargs = parser.read_conf(config)
    config.data.batch_size = 24
    assert config == args
    assert kwargs == Bunch(dict(config_name='test'))
