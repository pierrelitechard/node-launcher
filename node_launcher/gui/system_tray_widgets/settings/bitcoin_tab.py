from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QWidget, QLabel, QCheckBox, QVBoxLayout

from node_launcher.constants import Network, MAINNET, TESTNET
from .data_directories.data_directory_box import DataDirectoryBox
from node_launcher.node_set.litecoin import Litecoin


class LitecoinTab(QWidget):
    change_network = Signal(Network)

    def __init__(self, litecoin: Litecoin):
        super().__init__()

        self.litecoin = litecoin

        self.litecoin_layout = QVBoxLayout()

        self.data_directory_group_box = DataDirectoryBox(litecoin=self.litecoin)
        self.data_directory_group_box.file_dialog.new_data_directory.connect(
            self.change_datadir
        )

        self.litecoin_layout.addWidget(self.data_directory_group_box)
        self.litecoin_layout.setAlignment(self.data_directory_group_box, Qt.AlignHCenter)

        self.enable_wallet_label = QLabel('Enable wallet')
        self.enable_wallet_widget = QCheckBox('Enable Wallet')
        self.enable_wallet_widget.setChecked(not self.litecoin.file['disablewallet'])
        self.enable_wallet_widget.stateChanged.connect(
            lambda x: self.update_config('disablewallet', not bool(x))
        )
        self.litecoin_layout.addWidget(self.enable_wallet_widget)

        self.enable_testnet_label = QLabel('Enable testnet')
        self.enable_testnet_widget = QCheckBox('Enable Testnet')
        self.set_checked(
            self.enable_testnet_widget,
            self.litecoin.file['testnet']
        )
        self.enable_testnet_widget.stateChanged.connect(
            lambda x: self.update_config('testnet', bool(x))
        )
        self.litecoin_layout.addWidget(self.enable_testnet_widget)
        self.setLayout(self.litecoin_layout)
        self.litecoin.file.file_watcher.fileChanged.connect(self.litecoin_config_changed)

    def change_datadir(self, new_datadir: str):
        self.litecoin.file['datadir'] = new_datadir
        self.litecoin.set_prune()
        self.data_directory_group_box.set_datadir(
            self.litecoin.file['datadir'],
            self.litecoin.file['prune']
        )

    @staticmethod
    def set_checked(widget: QCheckBox, state: bool):
        if state is None:
            widget.setChecked(False)
            return
        widget.setChecked(state)

    def update_config(self, name: str, state: bool):
        self.litecoin.file[name] = state

        if name == 'testnet' and state:
            self.change_network.emit(TESTNET)
        elif name == 'testnet' and not state:
            self.change_network.emit(MAINNET)

    def litecoin_config_changed(self):
        if self.litecoin.file['testnet']:
            self.enable_testnet_widget.blockSignals(True)
            self.set_checked(self.enable_testnet_widget, True)
            self.enable_testnet_widget.blockSignals(False)
        else:
            self.enable_testnet_widget.blockSignals(True)
            self.set_checked(self.enable_testnet_widget, False)
            self.enable_testnet_widget.blockSignals(False)
