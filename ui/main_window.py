from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        layout.addWidget(self.tab_widget)
        
        self.tabs = {}
    
    def create_tabular_tab(self, norad_id, dataframe):
        tab_name = f"{norad_id}-Tabular"
        
        if tab_name in self.tabs:
            self.tab_widget.setCurrentWidget(self.tabs[tab_name])
            return
        
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
        
        self.tab_widget.addTab(table, tab_name)
        self.tabs[tab_name] = table
        self.tab_widget.setCurrentWidget(table)
    
    def close_tab(self, index):
        tab_name = self.tab_widget.tabText(index)
        widget = self.tab_widget.widget(index)
        self.tab_widget.removeTab(index)
        if tab_name in self.tabs:
            del self.tabs[tab_name]