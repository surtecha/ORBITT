from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt
from .dropdown_menu import DropdownMenu
from .tab import Tab
from styles.stylesheet import get_widget_style

class TopBar(QWidget):
    dropdown_changed = pyqtSignal(str)
    tab_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_dropdown_text = ""
        self.current_tab_name = ""
        self.tabs = {}
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(50)
        self.setStyleSheet(get_widget_style('topbar'))

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 5, 15, 5)
        main_layout.setSpacing(20)

        self.dropdown = DropdownMenu()
        self.dropdown.selection_changed.connect(self.on_dropdown_changed_by_user)
        main_layout.addWidget(self.dropdown)

        self.tab_container = QWidget()
        self.tab_layout = QHBoxLayout(self.tab_container)
        self.tab_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_layout.setSpacing(0)
        self.tab_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        main_layout.addWidget(self.tab_container)
        main_layout.addStretch(1)

        self.current_dropdown_text = self.dropdown.currentText()
        self._update_tabs_for_dropdown(self.current_dropdown_text)
        if self.tabs:
            first_tab_name = list(self.tabs.keys())[0]
            self.set_active_tab(first_tab_name, emit_signal=False)

    def on_dropdown_changed_by_user(self, dropdown_name):
        if self.current_dropdown_text != dropdown_name:
            self.current_dropdown_text = dropdown_name
            self._update_tabs_for_dropdown(dropdown_name)
            self.dropdown_changed.emit(dropdown_name)

            if self.tabs:
                first_tab_name = list(self.tabs.keys())[0]
                self.set_active_tab(first_tab_name, emit_signal=True)
            else:
                self.tab_changed.emit("")


    def _update_tabs_for_dropdown(self, dropdown_name):
        for tab_widget in self.tabs.values():
            self.tab_layout.removeWidget(tab_widget)
            tab_widget.deleteLater()
        self.tabs.clear()
        self.current_tab_name = ""

        tab_names = []
        if dropdown_name == "Visualize":
            tab_names = ["Plotter", "Extractor"]
        elif dropdown_name == "Neural Network":
            tab_names = ["Model Architecture"]

        for name in tab_names:
            tab_widget = Tab(name)
            tab_widget.clicked.connect(self.on_tab_widget_clicked)
            self.tabs[name] = tab_widget
            self.tab_layout.addWidget(tab_widget)
        
        self.tab_layout.addStretch(1)


    def on_tab_widget_clicked(self, tab_name):
        self.set_active_tab(tab_name, emit_signal=True)


    def set_active_dropdown(self, dropdown_name):
        if self.current_dropdown_text != dropdown_name:
            self.dropdown.set_selection(dropdown_name)

    def set_active_tab(self, tab_name, emit_signal=True):
        if self.current_tab_name == tab_name and self.tabs.get(tab_name, None) and self.tabs[tab_name].is_active :
             if emit_signal and tab_name:
                self.tab_changed.emit(tab_name)
             return

        self.current_tab_name = tab_name
        for name, tab_widget in self.tabs.items():
            tab_widget.set_active(name == tab_name)

        if emit_signal and tab_name:
            self.tab_changed.emit(tab_name)