import os

from node_launcher.node_set.lnd import (
    Lnd
)
from node_launcher.utilities.utilities import is_port_in_use


class TestDirectoryConfiguration(object):
    def test_lnd_data_path(self, lnd: Lnd):
        assert os.path.isdir(lnd.lnddir)

    def test_multi_property(self, lnd: Lnd):
        lnd.file['multi_property'] = [
            'test1',
            'test2'
        ]
        assert len(lnd.file['multi_property']) == 2

    def test_multi_listen(self, lnd: Lnd):
        lnd.file['listen'] = [
            '127.0.0.1:9835',
            '192.168.1.1:9736',
        ]
        assert lnd.node_port == '9835'

    def test_rest(self, lnd: Lnd):
        assert not is_port_in_use(lnd.rest_port)

    def test_node(self, lnd: Lnd):
        assert not is_port_in_use(lnd.node_port)

    def test_grpc(self, lnd: Lnd):
        assert not is_port_in_use(lnd.grpc_port)

    def test_litecoin_file_changed(self, lnd: Lnd):
        lnd.litecoin.file['rpcport'] = 9338
        lnd.litecoin.running = False
        lnd.litecoin.config_file_changed()
        lnd.litecoin_config_file_changed()
        new_config = lnd.file.snapshot
        lnd.running = False
        assert lnd.file['litecoind.rpchost'] == new_config['litecoind.rpchost'] == '127.0.0.1:9338'
        assert lnd.restart_required == False
        lnd.litecoin.running = True
        lnd.litecoin.config_snapshot = lnd.litecoin.file.snapshot
        assert lnd.litecoin.config_snapshot['rpcport'] == 9338
        lnd.litecoin.file['rpcport'] = 9340
        lnd.litecoin.config_file_changed()
        lnd.litecoin_config_file_changed()
        new_config = lnd.file.snapshot
        assert lnd.file['litecoind.rpchost'] == new_config['litecoind.rpchost'] == '127.0.0.1:9340'
        assert lnd.restart_required == False
        lnd.running = True
        assert lnd.litecoin.restart_required == True
        assert lnd.restart_required == True

    def test_file_changed(self, lnd: Lnd):
        lnd.file['listen'] = '127.0.0.1:9739'
        lnd.config_file_changed()
        lnd.running = False
        new_config = lnd.file.snapshot
        assert lnd.node_port == new_config['listen'].split(':')[-1] == '9739'
        assert lnd.restart_required == False
        lnd.running = True
        lnd.file['listen'] = '127.0.0.1:9741'
        lnd.config_file_changed()
        new_config = lnd.file.snapshot
        assert lnd.node_port == new_config['listen'].split(':')[-1] == '9741'
