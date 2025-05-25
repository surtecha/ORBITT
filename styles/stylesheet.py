MAIN_STYLESHEET = """
QMainWindow {
    background-color: white;
    color: black;
}

QWidget {
    background-color: white;
    color: black;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10px;
}

QLabel {
    color: black;
    background-color: transparent;
    border: none;
}

QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 11px;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #106ebe;
}

QPushButton:pressed {
    background-color: #005a9e;
}

QPushButton:disabled {
    background-color: #c0c0c0;
    color: #808080;
}

QLineEdit {
    background-color: white;
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 8px 12px;
    color: black;
    font-size: 10px;
}

QLineEdit:focus {
    border: 2px solid #0078d4;
    outline: none;
}

QLineEdit:hover {
    border: 1px solid #808080;
}

QTextEdit {
    background-color: white;
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 10px;
    color: black;
    font-size: 10px;
}

QTextEdit:focus {
    border: 2px solid #0078d4;
}

QComboBox {
    background-color: white;
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 5px 10px;
    color: black;
    font-size: 10px;
    min-height: 20px;
}

QComboBox:hover {
    border: 1px solid #0078d4;
}

QComboBox:focus {
    border: 2px solid #0078d4;
    outline: none;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid black;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: white;
    border: 1px solid #c0c0c0;
    selection-background-color: #e3f2fd;
    selection-color: black;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 8px 10px;
    border: none;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #f0f0f0;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #e3f2fd;
    color: black;
}

QSpinBox {
    background-color: white;
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 5px 10px;
    color: black;
    font-size: 10px;
    min-height: 20px;
}

QSpinBox:hover {
    border: 1px solid #0078d4;
}

QSpinBox:focus {
    border: 2px solid #0078d4;
}

QRadioButton {
    color: black;
    background: transparent;
    spacing: 8px;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
}

QRadioButton::indicator:unchecked {
    border: 2px solid #c0c0c0;
    border-radius: 8px;
    background-color: white;
}

QRadioButton::indicator:unchecked:hover {
    border: 2px solid #808080;
}

QRadioButton::indicator:checked {
    border: 2px solid #0078d4;
    border-radius: 8px;
    background-color: white;
}

QRadioButton::indicator:checked:after {
    width: 8px;
    height: 8px;
    border-radius: 4px;
    background-color: #0078d4;
    margin: 2px;
}

QCheckBox {
    color: black;
    background: transparent;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    border: 2px solid #c0c0c0;
    border-radius: 3px;
    background-color: white;
}

QCheckBox::indicator:unchecked:hover {
    border: 2px solid #808080;
}

QCheckBox::indicator:checked {
    border: 2px solid #0078d4;
    border-radius: 3px;
    background-color: #0078d4;
}

QCheckBox::indicator:checked:after {
    width: 6px;
    height: 10px;
    border: 2px solid white;
    border-top: none;
    border-left: none;
    margin: 1px;
}

QSlider::groove:horizontal {
    border: none;
    height: 4px;
    background: #e0e0e0;
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background: #0078d4;
    border: 2px solid white;
    width: 20px;
    height: 20px;
    margin: -10px 0;
    border-radius: 12px;
}

QSlider::handle:horizontal:hover {
    background: #106ebe;
    border: 2px solid white;
}

QSlider::handle:horizontal:pressed {
    background: #005a9e;
    border: 2px solid white;
}

QSlider::sub-page:horizontal {
    background: #0078d4;
    border-radius: 2px;
}

QSlider::groove:vertical {
    border: none;
    width: 4px;
    background: #e0e0e0;
    border-radius: 2px;
}

QSlider::handle:vertical {
    background: #0078d4;
    border: 2px solid white;
    width: 20px;
    height: 20px;
    margin: 0 -10px;
    border-radius: 12px;
}

QSlider::handle:vertical:hover {
    background: #106ebe;
    border: 2px solid white;
}

QSlider::handle:vertical:pressed {
    background: #005a9e;
    border: 2px solid white;
}

QSlider::sub-page:vertical {
    background: #0078d4;
    border-radius: 2px;
}

QScrollArea {
    background-color: white;
    border: none;
}

QScrollBar:vertical {
    background-color: #f0f0f0;
    width: 12px;
    border-radius: 6px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #c0c0c0;
    border-radius: 6px;
    min-height: 30px;
    margin: 0px;
}

QScrollBar::handle:vertical:hover {
    background-color: #a0a0a0;
}

QScrollBar::handle:vertical:pressed {
    background-color: #808080;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
    height: 0px;
}

QScrollBar:horizontal {
    background-color: #f0f0f0;
    height: 12px;
    border-radius: 6px;
    border: none;
}

QScrollBar::handle:horizontal {
    background-color: #c0c0c0;
    border-radius: 6px;
    min-width: 30px;
    margin: 0px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #a0a0a0;
}

QScrollBar::handle:horizontal:pressed {
    background-color: #808080;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
    width: 0px;
}

QGroupBox {
    font-weight: bold;
    font-size: 12px;
    color: black;
    border: 2px solid #d0d0d0;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 10px;
    background-color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 10px 0 10px;
    background-color: white;
    color: black;
}

QTabWidget::pane {
    border: 1px solid #d0d0d0;
    background-color: white;
}

QTabWidget::tab-bar {
    left: 5px;
}

QTabBar::tab {
    background-color: #f8f9fa;
    border: 1px solid #d0d0d0;
    padding: 8px 15px;
    margin-right: 2px;
    color: black;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom: 2px solid #0078d4;
    color: #0078d4;
}

QTabBar::tab:hover {
    background-color: #f0f0f0;
}

QSplitter::handle {
    background-color: #d0d0d0;
}

QSplitter::handle:horizontal {
    width: 3px;
}

QSplitter::handle:vertical {
    height: 3px;
}

QSplitter::handle:pressed {
    background-color: #0078d4;
}

QMenuBar {
    background-color: white;
    color: black;
    border-bottom: 1px solid #d0d0d0;
}

QMenuBar::item {
    padding: 5px 10px;
    background-color: transparent;
}

QMenuBar::item:selected {
    background-color: #e3f2fd;
    color: black;
}

QMenu {
    background-color: white;
    border: 1px solid #d0d0d0;
    color: black;
}

QMenu::item {
    padding: 8px 25px;
    background-color: transparent;
}

QMenu::item:selected {
    background-color: #e3f2fd;
    color: black;
}

QMenu::separator {
    height: 1px;
    background-color: #d0d0d0;
    margin: 5px 0px;
}

QStatusBar {
    background-color: #f8f9fa;
    color: black;
    border-top: 1px solid #d0d0d0;
}

QToolTip {
    background-color: white;
    color: black;
    border: 1px solid #d0d0d0;
    padding: 5px;
    border-radius: 3px;
}

QDialog {
    background-color: white;
    color: black;
}

QFrame {
    background-color: white;
    border: none;
}

QProgressBar {
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    text-align: center;
    background-color: #f0f0f0;
    color: black;
}

QProgressBar::chunk {
    background-color: #0078d4;
    border-radius: 3px;
}

QListWidget {
    background-color: white;
    border: 1px solid #c0c0c0;
    color: black;
    outline: none;
}

QListWidget::item {
    padding: 5px;
    border-bottom: 1px solid #f0f0f0;
}

QListWidget::item:selected {
    background-color: #e3f2fd;
    color: black;
}

QListWidget::item:hover {
    background-color: #f0f0f0;
}

QTreeWidget {
    background-color: white;
    border: 1px solid #c0c0c0;
    color: black;
    outline: none;
}

QTreeWidget::item {
    padding: 3px;
}

QTreeWidget::item:selected {
    background-color: #e3f2fd;
    color: black;
}

QTreeWidget::item:hover {
    background-color: #f0f0f0;
}

QTableWidget {
    background-color: white;
    border: 1px solid #c0c0c0;
    color: black;
    gridline-color: #e0e0e0;
    outline: none;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
    color: black;
}

QHeaderView::section {
    background-color: #f8f9fa;
    color: black;
    border: 1px solid #d0d0d0;
    padding: 5px;
    font-weight: bold;
}

QHeaderView::section:hover {
    background-color: #e0e0e0;
}
"""

BUTTON_STYLES = {
    'primary': """
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #106ebe;
        }
        QPushButton:pressed {
            background-color: #005a9e;
        }
        QPushButton:disabled {
            background-color: #c0c0c0;
            color: #808080;
        }
    """,
    
    'success': """
        QPushButton {
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #218838;
        }
        QPushButton:pressed {
            background-color: #1e7e34;
        }
        QPushButton:disabled {
            background-color: #c0c0c0;
            color: #808080;
        }
    """,
    
    'secondary': """
        QPushButton {
            background-color: #f0f0f0;
            color: black;
            border: 1px solid #c0c0c0;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
            border: 1px solid #808080;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        QPushButton:disabled {
            background-color: #f8f8f8;
            color: #c0c0c0;
            border: 1px solid #e0e0e0;
        }
    """,
    
    'danger': """
        QPushButton {
            background-color: #dc3545;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #c82333;
        }
        QPushButton:pressed {
            background-color: #bd2130;
        }
        QPushButton:disabled {
            background-color: #c0c0c0;
            color: #808080;
        }
    """
}

WIDGET_STYLES = {
    'sidebar': """
        QWidget {
            background-color: #f8f9fa;
            border-right: 1px solid #d0d0d0;
        }
    """,
    
    'topbar': """
        QWidget {
            background-color: white;
            border-bottom: 1px solid #d0d0d0;
        }
    """,
    
    'content': """
        QWidget {
            background-color: white;
            border-left: 1px solid #d0d0d0;
        }
    """,
    
    'card': """
        QWidget {
            background-color: white;
            border: 1px solid #d0d0d0;
            border-radius: 8px;
        }
    """,
    
    'card_hover': """
        QWidget {
            background-color: white;
            border: 2px solid #0078d4;
            border-radius: 8px;
        }
    """
}

def apply_main_stylesheet(app):
    app.setStyleSheet(MAIN_STYLESHEET)

def get_button_style(style_type='primary'):
    return BUTTON_STYLES.get(style_type, BUTTON_STYLES['primary'])

def get_widget_style(style_type):
    return WIDGET_STYLES.get(style_type, "")