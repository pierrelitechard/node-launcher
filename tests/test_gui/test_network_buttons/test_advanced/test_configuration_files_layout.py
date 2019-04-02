from unittest.mock import MagicMock, patch

import pytest
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from node_launcher.gui.system_tray_widgets import ConfigurationFilesLayout


@pytest.fixture
def actions_layout() -> ConfigurationFilesLayout:
    node_set = MagicMock()
    node_set.litecoin.file.directory = '/test/litecoin'
    node_set.lnd.file.directory = '/test/lnd'
    actions_layout = ConfigurationFilesLayout(node_set)
    return actions_layout


class TestActionsLayout(object):
    @patch('node_launcher.gui.system_tray_widgets.advanced.configuration_files_layout.reveal')
    def test_show_litecoin_conf(self,
                               reveal_patch: MagicMock,
                               actions_layout: ConfigurationFilesLayout,
                               qtbot: QTest):
        qtbot.mouseClick(actions_layout.show_litecoin_conf, Qt.LeftButton)
        reveal_patch.assert_called_with('/test/litecoin')

    @patch('node_launcher.gui.system_tray_widgets.advanced.configuration_files_layout.reveal')
    def test_show_lnd_conf(self,
                           reveal_patch: MagicMock,
                           actions_layout: ConfigurationFilesLayout,
                           qtbot: QTest):
        qtbot.mouseClick(actions_layout.show_lnd_conf, Qt.LeftButton)
        reveal_patch.assert_called_with('/test/lnd')
