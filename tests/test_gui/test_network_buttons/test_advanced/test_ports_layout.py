from unittest.mock import MagicMock

import pytest
from PySide2.QtTest import QTest

from node_launcher.constants import (
    LITECOIN_MAINNET_PEER_PORT,
    LND_DEFAULT_PEER_PORT,
    LITECOIN_MAINNET_RPC_PORT,
    LND_DEFAULT_GRPC_PORT,
    LND_DEFAULT_REST_PORT
)
from node_launcher.gui.network_buttons.advanced import PortsLayout


@pytest.fixture
def ports_layout():
    node_set = MagicMock()
    node_set.litecoin.node_port = LITECOIN_MAINNET_PEER_PORT
    node_set.litecoin.rpc_port = LITECOIN_MAINNET_RPC_PORT
    node_set.lnd.node_port = LND_DEFAULT_PEER_PORT
    node_set.lnd.grpc_port = LND_DEFAULT_GRPC_PORT
    node_set.lnd.rest_port = LND_DEFAULT_REST_PORT
    node_set.litecoin.zmq_block_port = 19500
    node_set.litecoin.zmq_tx_port = 19501
    ports_layout = PortsLayout(node_set)
    return ports_layout


class TestPortsLayout(object):
    def test_litecoin_network_port(self,
                                  ports_layout: PortsLayout,
                                  qtbot: QTest):
        assert ports_layout.litecoin_network_port.text().endswith(
            str(LITECOIN_MAINNET_PEER_PORT)
        )

    def test_lnd_network_port(self,
                              ports_layout: PortsLayout,
                              qtbot: QTest):
        assert ports_layout.lnd_network_port.text().endswith(
            str(LND_DEFAULT_PEER_PORT)
        )

    def test_zmq_ports(self,
                       ports_layout: PortsLayout,
                       qtbot: QTest):
        assert ports_layout.zmq_ports.text().endswith('19500/19501')

    def test_rpc_port(self,
                       ports_layout: PortsLayout,
                       qtbot: QTest):
        assert ports_layout.rpc_port.text().endswith(
            str(LITECOIN_MAINNET_RPC_PORT)
        )

    def test_grpc_port(self,
                      ports_layout: PortsLayout,
                      qtbot: QTest):
        assert ports_layout.grpc_port.text().endswith(
            str(LND_DEFAULT_GRPC_PORT)
        )

    def test_rest_port(self,
                       ports_layout: PortsLayout,
                       qtbot: QTest):
        assert ports_layout.rest_port.text().endswith(
            str(LND_DEFAULT_REST_PORT)
        )
