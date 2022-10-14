import pytest

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


@pytest.fixture
def mock_open_config(mocker):
    mocker.patch("__builtin__.open", mocker.mock_open(read_data=TEST_CONFIG_FILE))
