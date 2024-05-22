from ..argparse_config import ArgparseConfig
from ..bunch import Bunch


TEST_CONFIG_DICT = {
        'default': {'opt': {'optimizer': 'adam', 'lr': 1, 'regularizer': True},
              'data': {'dataset': 'ns', 'batch_size': 12, 'test_resolutions':[16,32]}},
        'test': {'opt': {'optimizer': 'SGD'}}
}


def test_ArgparseConfig(monkeypatch):
    monkeypatch.setattr("sys.argv", ['test', '--data.batch_size', '24',\
                                            '--data.test_resolutions', '[16]'])
    config = Bunch(TEST_CONFIG_DICT['default'])
    parser = ArgparseConfig(infer_types='fuzzy')
    args, kwargs = parser.read_conf(config)
    assert args.data.test_resolutions == [16]
    config.data.batch_size = 24
    config.data.test_resolutions = [16]
    assert config == args
    # reset config data test_res
    config.data.test_resolutions = [16,32]
    assert kwargs == {}
    
    # test ability to infer None, int-->float and iterables
    monkeypatch.setattr("sys.argv", ['test', '--data.batch_size', '24',\
                                    '--data.test_resolutions', '[8, None]',\
                                     '--opt.lr', '0.01',\
                                     '--opt.regularizer', 'False',\
                                     '--config_name', 'test'])
    config = Bunch(TEST_CONFIG_DICT['default'])
    parser = ArgparseConfig(infer_types='fuzzy', config_name=None)
    args, kwargs = parser.read_conf(config)
    config.data.batch_size = 24
    assert args.opt.lr == 0.01 # ensure no casting to int
    assert args.data.test_resolutions == [8, None]
    assert not args.opt.regularizer #boolean False, not 'False'


    args.data.test_resolutions = [16,32]
    args.opt.regularizer = True
    args.opt.lr = 1
    assert config == args
    assert kwargs == Bunch(dict(config_name='test'))

    # Test overwriting entire nested argument
    monkeypatch.setattr("sys.argv", ['test', '--data', '0', '--config_name', 'test'])
    config = Bunch(TEST_CONFIG_DICT['default'])
    parser = ArgparseConfig(infer_types='fuzzy', config_name=None, overwrite_nested_config=True)
    args, kwargs = parser.read_conf(config)
    config['data'] = 0
    assert config == args
    assert kwargs == Bunch(dict(config_name='test'))
