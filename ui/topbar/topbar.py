from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from .dropdown_menu import DropdownMenu
from .tab import Tab

class TopBar(QWidget):
    dropdown_changed = pyqtSignal(str)
    tab_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_dropdown = None
        self.current_tab = None
        self.tabs = {}
        self.init_ui()
        
    def init_ui(self):
        self.setFixedHeight(80)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #d0d0d0;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        top_section = QWidget()
        top_section.setFixedHeight(40)
        top_layout = QHBoxLayout(top_section)
        top_layout.setContentsMargins(10, 5, 10, 5)
        
        self.dropdown = DropdownMenu()
        self.dropdown.selection_changed.connect(self.on_dropdown_changed)
        top_layout.addWidget(self.dropdown)
        top_layout.addStretch()
        
        self.tab_container = QWidget()
        self.tab_container.setFixedHeight(40)
        self.tab_layout = QHBoxLayout(self.tab_container)
        self.tab_layout.setContentsMargins(10, 0, 10, 0)
        self.tab_layout.setSpacing(2)
        self.tab_layout.addStretch()
        
        main_layout.addWidget(top_section)
        main_layout.addWidget(self.tab_container)
        
    def on_dropdown_changed(self, dropdown_name):
        self.current_dropdown = dropdown_name
        self.update_tabs()
        self.dropdown_changed.emit(dropdown_name)
        
    def update_tabs(self):
        for tab in self.tabs.values():
            tab.hide()
            
        self.tabs.clear()
        
        if self.current_dropdown == "Visualize":
            tab_names = ["Plotter", "Extractor"]
        elif self.current_dropdown == "Neural Network":
            tab_names = ["Model Architecture"]
        else:
            tab_names = []
            
        for name in tab_names:
            tab = Tab(name)
            tab.clicked.connect(lambda n=name: self.on_tab_clicked(n))
            self.tabs[name] = tab
            self.tab_layout.insertWidget(self.tab_layout.count() - 1, tab)
            
        if tab_names:
            first_tab = tab_names[0]
            self.set_active_tab(first_tab)
            
    def on_tab_clicked(self, tab_name):
        self.set_active_tab(tab_name)
        self.tab_changed.emit(tab_name)
        
    def set_active_dropdown(self, dropdown_name):
        self.dropdown.set_selection(dropdown_name)
        
    def set_active_tab(self, tab_name):
        self.current_tab = tab_name
        for name, tab in self.tabs.items():
            tab.set_active(name == tab_name)