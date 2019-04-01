import pytest
from tempfile import NamedTemporaryFile

from node_launcher.constants import Network, TESTNET
from node_launcher.node_set.lnd import Lnd
from node_launcher.node_set.lnd_client import LndClient
from node_launcher.node_set import NodeSet
from node_launcher.node_set.litecoin import Litecoin
from node_launcher.gui.main_widget import MainWidget


@pytest.fixture
def network() -> Network:
    return TESTNET


@pytest.fixture
def litecoin(network: str) -> Litecoin:
    with NamedTemporaryFile(suffix='-litecoin.conf', delete=False) as f:
        litecoin = Litecoin(configuration_file_path=f.name)
    return litecoin


@pytest.fixture
def lnd(network: str, litecoin: Litecoin) -> Lnd:
    with NamedTemporaryFile(suffix='-lnd-ltc.conf', delete=False) as f:
        lnd = Lnd(configuration_file_path=f.name,
                  litecoin=litecoin)
    return lnd


@pytest.fixture
def node_set(network: str,
             litecoin: Litecoin,
             lnd: Lnd) -> NodeSet:
    configuration = NodeSet()
    return configuration


@pytest.fixture
def lnd_client(lnd: Lnd) -> LndClient:
    lnd_client = LndClient(lnd)
    return lnd_client


@pytest.fixture
def main_widget():
    main_widget = MainWidget()
    return main_widget
