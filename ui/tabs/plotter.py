from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import QObject, Signal
from ui.components.input_field import InputField
from ui.components.radio_button_group import RadioButtonGroup
from ui.components.slider_input_field import SliderInputField
from core.plotting.plot_manager import PlotManager


class PlotterLogic(QObject):
    data_updated = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.plot_manager = PlotManager()
        self.norad_input = None
        self.time_filter = None
        self.time_slider = None
        self.plot_button = None
        self.last_epoch_label = None
        self.tles_count_label = None
        self.total_tles_label = None
        self.main_widget = None

    def setup_widgets(self):
        self.norad_input = InputField("NORAD ID", "")
        self.time_filter = RadioButtonGroup("Time Filter", options=["D", "W", "M"], default_option="D")
        self.time_slider = SliderInputField("Days Back", min_value=1, max_value=100, step=1, default=60)
        self.plot_button = QPushButton("Plot")

        self.last_epoch_label = QLabel("Last Epoch: N/A")
        self.tles_count_label = QLabel("TLEs Obtained: 0")
        self.total_tles_label = QLabel("Total TLEs: 0")

        self.plot_button.clicked.connect(self.create_plots)

        return ([self.norad_input, self.time_filter, self.time_slider, self.plot_button],
                [self.last_epoch_label, self.tles_count_label, self.total_tles_label])

    def set_main_widget(self, widget):
        self.main_widget = widget

    def create_plots(self):
        norad_id = self.norad_input.text().strip()
        if not norad_id:
            QMessageBox.warning(None, "Warning", "Please enter a NORAD ID")
            return

        from config.data_config import DataConfig
        config = DataConfig()
        data_dir = config.get_data_directory()

        if not data_dir:
            QMessageBox.warning(None, "Warning", "Please select a data directory first")
            return

        if not self.plot_manager.load_data(data_dir, norad_id):
            QMessageBox.warning(None, "Error", f"No data found for NORAD ID: {norad_id}")
            return

        timeframe = self.time_filter.selected()
        days_back = self.time_slider.value()

        if not self.plot_manager.filter_data(timeframe, days_back):
            QMessageBox.warning(None, "Warning", "No data available for the selected time range")
            return

        last_epoch, filtered_tles, total_tles = self.plot_manager.get_data_info()
        self.last_epoch_label.setText(f"Last Epoch: {last_epoch}")
        self.tles_count_label.setText(f"TLEs Obtained: {filtered_tles}")
        self.total_tles_label.setText(f"Total TLEs: {total_tles}")

        if self.main_widget:
            plot_widget = self.plot_manager.create_plot_tiles(self.main_widget)
            layout = self.main_widget.layout()

            if layout.count() > 0:
                old_widget = layout.itemAt(0).widget()
                if old_widget:
                    old_widget.setParent(None)

            layout.addWidget(plot_widget)


_plotter_logic = PlotterLogic()


def get_tab_widget():
    widget = QWidget()
    layout = QVBoxLayout(widget)
    _plotter_logic.set_main_widget(widget)
    return widget


def get_sidebar_widgets():
    return _plotter_logic.setup_widgets()