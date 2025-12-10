from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt


class TabManager(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self._close_tab)

        layout.addWidget(self.tab_widget)

        self.tabs = {}

    def create_tabular_tab(self, satellite_id, name, dataframe):
        tab_key = f"{satellite_id}-Tabular"

        if tab_key in self.tabs:
            self.tab_widget.setCurrentWidget(self.tabs[tab_key]['widget'])
            return

        table = self._create_table(dataframe)

        tab_name = f"{name}-Tabular"
        self.tab_widget.addTab(table, tab_name)
        self.tabs[tab_key] = {'widget': table, 'satellite_id': satellite_id, 'type': 'Tabular'}
        self.tab_widget.setCurrentWidget(table)

    def _create_table(self, dataframe):
        table = QTableWidget()
        table.setRowCount(len(dataframe))
        table.setColumnCount(len(dataframe.columns))
        table.setHorizontalHeaderLabels(dataframe.columns.tolist())

        for i, row in dataframe.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(i, j, item)

        table.resizeColumnsToContents()
        return table

    def _close_tab(self, index):
        widget = self.tab_widget.widget(index)
        tab_key = next((k for k, v in self.tabs.items() if v['widget'] == widget), None)

        self.tab_widget.removeTab(index)
        if tab_key:
            del self.tabs[tab_key]

    def close_tabs_for_satellite(self, satellite_id):
        tabs_to_remove = [k for k, v in self.tabs.items() if v['satellite_id'] == satellite_id]

        for tab_key in tabs_to_remove:
            widget = self.tabs[tab_key]['widget']
            index = self.tab_widget.indexOf(widget)
            if index >= 0:
                self.tab_widget.removeTab(index)
            del self.tabs[tab_key]

    def update_tab_names(self, satellite_id, new_name):
        for tab_key, tab_info in self.tabs.items():
            if tab_info['satellite_id'] == satellite_id:
                widget = tab_info['widget']
                index = self.tab_widget.indexOf(widget)
                if index >= 0:
                    tab_type = tab_info['type']
                    self.tab_widget.setTabText(index, f"{new_name}-{tab_type}")