from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import QKeySequence, QClipboard
from PySide2.QtWidgets import QMenu

from node_launcher.constants import LITECOIN_CLI_COMMANDS, LNCLI_COMMANDS
from node_launcher.gui.system_tray_widgets import (
    AdvancedWidget,
    LitecoindOutputWidget,
    ConsoleDialog,
    LndOutputWidget,
    SettingsTabDialog
)
from node_launcher.gui.utilities import reveal
from node_launcher.node_set import NodeSet


class Menu(QMenu):
    def __init__(self, node_set: NodeSet, system_tray):
        super().__init__()
        self.node_set = node_set
        self.system_tray = system_tray

        self.litecoind_status_action = self.addAction('litecoind off')
        self.litecoind_status_action.setEnabled(False)

        # litecoin console
        self.litecoin_cli_widget = ConsoleDialog(
            title='litecoin-cli',
            program=self.node_set.litecoin.software.litecoin_cli,
            args=self.node_set.litecoin.args,
            commands=LITECOIN_CLI_COMMANDS
        )
        self.litecoin_console_action = self.addAction('Open Litecoin Console')
        self.litecoin_console_action.triggered.connect(
            self.litecoin_cli_widget.show
        )

        # litecoind output
        self.litecoind_output_widget = LitecoindOutputWidget(
            node_set=self.node_set,
            system_tray=self.system_tray
        )
        self.litecoind_output_action = self.addAction('See Litecoin Output')
        self.litecoind_output_action.triggered.connect(
            self.litecoind_output_widget.show
        )

        self.addSeparator()

        self.lnd_status_action = self.addAction('lnd off')
        self.lnd_status_action.setEnabled(False)

        # lnd console

        self.lncli_widget = ConsoleDialog(
            title='lncli',
            program=self.node_set.lnd.software.lncli,
            args=self.node_set.lnd.lncli_arguments(),
            commands=LNCLI_COMMANDS
        )
        self.lnd_console_action = self.addAction('Open LND Console')
        self.lnd_console_action.triggered.connect(
            self.lncli_widget.show
        )

        # lnd output
        self.lnd_output_widget = LndOutputWidget(
            node_set=self.node_set,
            system_tray=self.system_tray
        )
        self.lnd_output_action = self.addAction('See LND Output')
        self.lnd_output_action.triggered.connect(
            self.lnd_output_widget.show
        )

        self.addSeparator()

        # Joule

        self.joule_status_action = self.addAction('Joule Browser Extension')
        self.joule_status_action.setEnabled(False)
        self.joule_url_action = self.addAction('Copy Node URL (REST)')
        self.joule_macaroons_action = self.addAction('Show Macaroons')

        self.joule_url_action.triggered.connect(
            lambda: QClipboard().setText(self.node_set.lnd.rest_url)
        )

        self.joule_macaroons_action.triggered.connect(
            lambda: reveal(self.node_set.lnd.macaroon_path)
        )

        self.addSeparator()

        # settings

        self.settings_action = self.addAction('&Settings')
        self.settings_action.setShortcut(QKeySequence.Preferences)
        self.settings_tab = SettingsTabDialog(node_set=self.node_set)
        self.settings_action.triggered.connect(self.settings_tab.show)

        # advanced

        self.advanced_widget = AdvancedWidget(node_set=self.node_set)
        self.advanced_action = self.addAction('Advanced...')
        self.advanced_action.triggered.connect(self.advanced_widget.show)

        self.addSeparator()

        # quit
        self.quit_action = self.addAction('Quit')

        self.quit_action.triggered.connect(
            lambda _: QCoreApplication.exit(0)
        )
