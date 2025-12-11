from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from ui.tabs.tabular_tab import create_tabular_widget


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

        table = create_tabular_widget(dataframe)

        tab_name = f"{name}-Tabular"
        self.tab_widget.addTab(table, tab_name)
        self.tabs[tab_key] = {'widget': table, 'satellite_id': satellite_id, 'type': 'Tabular'}
        self.tab_widget.setCurrentWidget(table)

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
        # Iterate through a copy of items to avoid issues during iteration
        for tab_key, tab_info in list(self.tabs.items()):
            if tab_info['satellite_id'] == satellite_id:
                widget = tab_info['widget']
                index = self.tab_widget.indexOf(widget)
                if index >= 0:
                    tab_type = tab_info['type']
                    new_tab_name = f"{new_name}-{tab_type}"
                    self.tab_widget.setTabText(index, new_tab_name)
        
        self.tab_widget.update()