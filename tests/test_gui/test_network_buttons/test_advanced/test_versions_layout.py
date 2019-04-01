from unittest.mock import MagicMock

import pytest
from PySide2.QtTest import QTest

from node_launcher.constants import (
    NODE_LAUNCHER_RELEASE,
    TARGET_LITECOIN_RELEASE,
    TARGET_LND_RELEASE
)
from node_launcher.gui.network_buttons.advanced import VersionsLayout


@pytest.fixture
def versions_layout():
    node_set = MagicMock()
    node_set.litecoin.software.release_version = TARGET_LITECOIN_RELEASE
    node_set.lnd.software.release_version = TARGET_LND_RELEASE
    versions_layout = VersionsLayout(node_set)
    return versions_layout


class TestVersionsLayout(object):
    def test_node_launcher_version(self,
                                   versions_layout: VersionsLayout,
                                   qtbot: QTest):
        assert versions_layout.node_launcher_version.text().endswith(
            NODE_LAUNCHER_RELEASE
        )

    def test_litecoin_version(self,
                             versions_layout: VersionsLayout,
                             qtbot: QTest):
        assert versions_layout.litecoin_version.text().endswith(
            TARGET_LITECOIN_RELEASE
        )

    def test_lnd_version(self,
                         versions_layout: VersionsLayout,
                         qtbot: QTest):
        assert versions_layout.lnd_version.text().endswith(
            TARGET_LND_RELEASE
        )
