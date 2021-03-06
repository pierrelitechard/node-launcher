from PySide2.QtCore import QTimer
from node_launcher.gui.components.grid_layout import QGridLayout
from node_launcher.gui.components.section_name import SectionName
from node_launcher.node_set import NodeSet
from node_launcher.gui.components.warning_text import WarningText


class RestartLayout(QGridLayout):
    node_set: NodeSet
    timer = QTimer

    def __init__(self, node_set: NodeSet):
        super(RestartLayout, self).__init__()

        self.timer = QTimer(self.parentWidget())

        self.node_set = node_set
        columns = 2

        self.section_name = SectionName('Restart Required')
        self.addWidget(self.section_name, column_span=columns)
        self.litecoin_restart_required = WarningText('Litecoin: ')
        self.lnd_restart_required = WarningText('Lnd: ')
        self.addWidget(self.litecoin_restart_required)
        self.addWidget(self.lnd_restart_required, same_row=True, column=columns)
        self.litecoin_restart_required.hide()
        self.lnd_restart_required.hide()
        self.node_set.litecoin.file.file_watcher.fileChanged.connect(self.check_restart_required)
        self.node_set.lnd.file.file_watcher.fileChanged.connect(self.check_restart_required)
        self.timer.start(1000)
        self.timer.timeout.connect(self.check_restart_required)

    def check_restart_required(self):
        restart_required = self.node_set.litecoin.restart_required or self.node_set.lnd.restart_required

        self.litecoin_restart_required.setText(f'Litecoin: {self.node_set.litecoin.restart_required}')
        self.lnd_restart_required.setText(f'Lnd: {self.node_set.lnd.restart_required}')
        if restart_required:
            self.section_name.show()
            self.litecoin_restart_required.show()
            self.lnd_restart_required.show()
        else:
            self.section_name.hide()
            self.litecoin_restart_required.hide()
            self.lnd_restart_required.hide()
