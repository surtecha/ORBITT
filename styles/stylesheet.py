def get_widget_style(widget_type):
    styles = {
        'topbar': """
            QWidget {
                background-color: #ffffff;
                border-bottom: 1px solid #e5e7eb;
            }
        """,
        
        'sidebar': """
            QWidget {
                background-color: #f8fafc;
                border-right: 1px solid #e5e7eb;
            }
            
            QLabel#sidebarTitleLabel {
                font-size: 18px;
                font-weight: 600;
                color: #1f2937;
                margin-bottom: 5px;
            }
            
            QGroupBox {
                font-size: 14px;
                font-weight: 500;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: #ffffff;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: #374151;
                background-color: #ffffff;
            }
        """,
        
        'content': """
            QWidget {
                background-color: #ffffff;
            }
        """,
        
        'card': """
            QWidget {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
            
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #374151;
                background-color: transparent;
                border: none;
            }
        """,
        
        'card_hover': """
            QWidget {
                background-color: #f9fafb;
                border: 1px solid #3b82f6;
                border-radius: 12px;
            }
            
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #1f2937;
                background-color: transparent;
                border: none;
            }
        """,
        
        'chart_placeholder': """
            QWidget {
                background-color: #f9fafb;
                border: none;
                border-radius: 8px;
            }
        """,
        
        'fullscreen_header': """
            QWidget {
                background-color: #ffffff;
                border-bottom: 1px solid #e5e7eb;
            }
            
            QLabel#fullscreenPlotTitleLabel {
                font-size: 20px;
                font-weight: 600;
                color: #1f2937;
            }
        """,
        
        'fullscreen_controls': """
            QWidget {
                background-color: #f8fafc;
                border-top: 1px solid #e5e7eb;
            }
            
            QLabel#fullscreenControlsLabel {
                font-size: 14px;
                font-weight: 500;
                color: #374151;
            }
            
            QLabel#fullscreenInfoLabel {
                font-size: 12px;
                color: #6b7280;
            }
        """,
        
        'labeled_output': """
            QLabel {
                font-size: 13px;
                color: #374151;
                background-color: #f9fafb;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 8px 12px;
                min-height: 20px;
            }
        """
    }
    
    return styles.get(widget_type, "")

def get_button_style(button_type):
    styles = {
        'primary': """
            QPushButton {
                background-color: #3b82f6;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                min-height: 16px;
            }
            
            QPushButton:hover {
                background-color: #2563eb;
            }
            
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            
            QPushButton:disabled {
                background-color: #9ca3af;
                color: #d1d5db;
            }
        """,
        
        'secondary': """
            QPushButton {
                background-color: #ffffff;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                min-height: 16px;
            }
            
            QPushButton:hover {
                background-color: #f9fafb;
                border-color: #9ca3af;
            }
            
            QPushButton:pressed {
                background-color: #f3f4f6;
            }
            
            QPushButton:disabled {
                background-color: #f9fafb;
                color: #9ca3af;
                border-color: #e5e7eb;
            }
        """,
        
        'success': """
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
                min-height: 16px;
            }
            
            QPushButton:hover {
                background-color: #059669;
            }
            
            QPushButton:pressed {
                background-color: #047857;
            }
            
            QPushButton:disabled {
                background-color: #9ca3af;
                color: #d1d5db;
            }
        """,
        
        'button_small_primary': """
            QPushButton {
                background-color: #3b82f6;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
                min-height: 12px;
            }
            
            QPushButton:hover {
                background-color: #2563eb;
            }
            
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """,
        
        'button_small_secondary': """
            QPushButton {
                background-color: #ffffff;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 500;
                min-height: 12px;
            }
            
            QPushButton:hover {
                background-color: #f9fafb;
                border-color: #9ca3af;
            }
            
            QPushButton:pressed {
                background-color: #f3f4f6;
            }
        """
    }
    
    return styles.get(button_type, "")

def get_tab_style(is_active):
    if is_active:
        return """
            QWidget {
                background-color: #ffffff;
                border-bottom: 2px solid #3b82f6;
                padding: 8px 16px;
                margin: 0px;
            }
            
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #3b82f6;
            }
        """
    else:
        return """
            QWidget {
                background-color: transparent;
                border-bottom: 2px solid transparent;
                padding: 8px 16px;
                margin: 0px;
            }
            
            QWidget:hover {
                background-color: #f9fafb;
            }
            
            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #6b7280;
            }
            
            QLabel:hover {
                color: #374151;
            }
        """

def get_dropdown_style():
    return """
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 14px;
            font-weight: 500;
            color: #374151;
            min-height: 16px;
        }
        
        QComboBox:hover {
            border-color: #9ca3af;
        }
        
        QComboBox:focus {
            border-color: #3b82f6;
            outline: none;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #6b7280;
            width: 0px;
            height: 0px;
        }
        
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            selection-background-color: #f3f4f6;
            selection-color: #1f2937;
            outline: none;
            padding: 4px;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            border-radius: 4px;
            min-height: 16px;
        }
        
        QComboBox QAbstractItemView::item:hover {
            background-color: #f9fafb;
        }
        
        QComboBox QAbstractItemView::item:selected {
            background-color: #f3f4f6;
        }
    """

def get_input_style():
    return """
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 10px 12px;
            font-size: 14px;
            color: #374151;
            selection-background-color: #dbeafe;
            min-height: 16px;
        }
        
        QLineEdit:focus {
            border-color: #3b82f6;
            outline: none;
        }
        
        QLineEdit:disabled {
            background-color: #f9fafb;
            color: #9ca3af;
            border-color: #e5e7eb;
        }
    """

def get_radio_button_style():
    return """
        QRadioButton {
            font-size: 14px;
            color: #374151;
            spacing: 8px;
            padding: 4px;
        }
        
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border-radius: 8px;
            border: 2px solid #d1d5db;
            background-color: #ffffff;
        }
        
        QRadioButton::indicator:hover {
            border-color: #9ca3af;
        }
        
        QRadioButton::indicator:checked {
            border-color: #3b82f6;
            background-color: #3b82f6;
        }
        
        QRadioButton::indicator:checked::after {
            content: "";
            width: 6px;
            height: 6px;
            border-radius: 3px;
            background-color: #ffffff;
            margin: 3px;
        }
    """

def get_slider_style():
    return """
        QSlider::groove:horizontal {
            border: none;
            height: 6px;
            background-color: #e5e7eb;
            border-radius: 3px;
        }
        
        QSlider::handle:horizontal {
            background-color: #3b82f6;
            border: none;
            width: 18px;
            height: 18px;
            margin: -6px 0;
            border-radius: 9px;
        }
        
        QSlider::handle:horizontal:hover {
            background-color: #2563eb;
        }
        
        QSlider::handle:horizontal:pressed {
            background-color: #1d4ed8;
        }
        
        QSlider::sub-page:horizontal {
            background-color: #3b82f6;
            border-radius: 3px;
        }
    """

def get_text_edit_style():
    return """
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 12px;
            font-size: 13px;
            color: #374151;
            font-family: 'Segoe UI', Arial, sans-serif;
            selection-background-color: #dbeafe;
        }
        
        QTextEdit:focus {
            border-color: #3b82f6;
            outline: none;
        }
        
        QTextEdit:disabled {
            background-color: #f9fafb;
            color: #9ca3af;
            border-color: #e5e7eb;
        }
    """

def get_progress_bar_style():
    return """
        QProgressBar {
            border: 1px solid #d1d5db;
            border-radius: 8px;
            text-align: center;
            font-size: 12px;
            color: #374151;
            font-weight: 500;
            background-color: #f9fafb;
            min-height: 20px;
        }
        
        QProgressBar::chunk {
            background-color: #3b82f6;
            border-radius: 7px;
            margin: 1px;
        }
    """

def get_scroll_area_style():
    return """
        QScrollArea {
            border: none;
            background-color: transparent;
        }
        
        QScrollBar:vertical {
            background-color: #f9fafb;
            width: 8px;
            border-radius: 4px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #d1d5db;
            border-radius: 4px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #9ca3af;
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            background-color: #f9fafb;
            height: 8px;
            border-radius: 4px;
            margin: 0px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #d1d5db;
            border-radius: 4px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #9ca3af;
        }
        
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            width: 0px;
        }
    """

def get_label_styles():
    return """
        QLabel#categoryTitleLabel {
            font-size: 20px;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 10px;
        }
        
        QLabel#extractorTitleLabel {
            font-size: 24px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 20px;
        }
        
        QLabel#valueLabel {
            font-size: 14px;
            font-weight: 600;
            color: #374151;
            min-width: 20px;
        }
        
        QLabel#minLabel, QLabel#maxLabel {
            font-size: 12px;
            color: #6b7280;
        }
    """

def apply_global_styles(app):
    dropdown_style = get_dropdown_style()
    input_style = get_input_style()
    radio_style = get_radio_button_style()
    slider_style = get_slider_style()
    text_edit_style = get_text_edit_style()
    progress_style = get_progress_bar_style()
    scroll_style = get_scroll_area_style()
    label_styles = get_label_styles()
    
    global_style = f"""
        {dropdown_style}
        {input_style}
        {radio_style}
        {slider_style}
        {text_edit_style}
        {progress_style}
        {scroll_style}
        {label_styles}
        
        QWidget {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            font-size: 14px;
        }}
        
        QMainWindow {{
            background-color: #ffffff;
        }}
        
        QMessageBox {{
            background-color: #ffffff;
            color: #374151;
        }}
        
        QMessageBox QPushButton {{
            background-color: #3b82f6;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
            min-width: 60px;
        }}
        
        QMessageBox QPushButton:hover {{
            background-color: #2563eb;
        }}
        
        QFileDialog {{
            background-color: #ffffff;
            color: #374151;
        }}
    """
    
    app.setStyleSheet(global_style)