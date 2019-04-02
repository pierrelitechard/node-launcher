import os
from tempfile import TemporaryDirectory

from node_launcher.constants import (
    MAINNET_PRUNE,
    TESTNET_PRUNE
)
from node_launcher.node_set.litecoin import Litecoin
from node_launcher.services.configuration_file import ConfigurationFile


class TestLitecoinConfiguration(object):
    @staticmethod
    def test_configuration_path_no_directory():
        with TemporaryDirectory() as tmpdirname:
            os.rmdir(tmpdirname)
            configuration_path = os.path.join(tmpdirname, 'litecoin.conf')
            litecoin = Litecoin(configuration_file_path=configuration_path)
            assert os.path.isfile(litecoin.file.path)

    @staticmethod
    def test_configuration_path(litecoin: Litecoin):
        assert litecoin.file.path.endswith('litecoin.conf')
        assert os.path.isfile(litecoin.file.path)

    @staticmethod
    def test_datadir(litecoin: Litecoin):
        assert os.path.exists(litecoin.file['datadir'])
        assert 'litecoin.conf' in os.listdir(litecoin.file['datadir'])

    @staticmethod
    def test_prune(litecoin: Litecoin):
        assert (
                litecoin.file['prune'] == TESTNET_PRUNE
                or litecoin.file['prune'] == 0
                or litecoin.file['prune'] == MAINNET_PRUNE
        )

    @staticmethod
    def test_set_prune(litecoin: Litecoin):
        litecoin.set_prune(True)
        pruned = ConfigurationFile(litecoin.file.path)
        assert pruned['prune']
        assert not pruned['txindex']
        litecoin.set_prune(False)
        unpruned = ConfigurationFile(litecoin.file.path)
        assert not unpruned['prune']
        assert unpruned['txindex']

    @staticmethod
    def test_rpcuser(litecoin: Litecoin):
        assert litecoin.file['rpcuser']

    @staticmethod
    def test_set_rpcuser(litecoin: Litecoin):
        litecoin.file['rpcuser'] = 'test_user'
        changed = ConfigurationFile(litecoin.file.path)
        assert changed['rpcuser'] == 'test_user'
        litecoin.file['rpcuser'] = 'test_user_2'
        changed_again = ConfigurationFile(litecoin.file.path)
        assert changed_again['rpcuser'] == 'test_user_2'

    @staticmethod
    def test_autoconfigure_datadir(litecoin: Litecoin):
        datadir = litecoin.file['datadir']
        prune = litecoin.file['prune']
        txindex = litecoin.file['txindex']
        assert datadir
        assert prune != txindex

    def test_file_changed(self, litecoin: Litecoin):
        litecoin.file['rpcport'] = 8338
        litecoin.config_file_changed()
        new_config = litecoin.file.snapshot
        litecoin.running = False
        assert litecoin.rpc_port == new_config['rpcport'] == new_config['main.rpcport'] == 8338
        assert litecoin.restart_required == False
        litecoin.running = True
        assert litecoin.restart_required == True
        litecoin.file['port'] = 8336
        litecoin.config_file_changed()
        new_config = litecoin.file.snapshot
        litecoin.running = False
        assert litecoin.node_port == new_config['port'] == new_config['main.port'] == 8336
        assert litecoin.restart_required == False
        litecoin.running = True
        assert litecoin.restart_required == True

