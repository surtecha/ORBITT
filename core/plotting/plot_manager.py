from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel
from ui.components.tile import Tile
from core.plotting.plot_utils import load_satellite_data, filter_data_by_timeframe, create_preview_plot, get_plot_sections
from ui.dialogs.plot_window import PlotWindow


class PlotManager(QObject):
    plots_updated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_data = None
        self.filtered_data = None
        self.plot_sections = get_plot_sections()

    def load_data(self, data_dir, norad_id):
        self.current_data = load_satellite_data(data_dir, norad_id)
        return self.current_data is not None

    def filter_data(self, timeframe, days_back):
        if self.current_data is None:
            return False
        self.filtered_data = filter_data_by_timeframe(self.current_data, timeframe, days_back)
        return len(self.filtered_data) > 0

    def create_plot_tiles(self, parent_widget):
        if self.filtered_data is None or len(self.filtered_data) == 0:
            return QLabel("No data available")

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        for section_name, section_data in self.plot_sections.items():
            section_label = QLabel(f"<b>{section_name}</b>")
            section_label.setStyleSheet("font-size: 14px; margin: 10px 0px 5px 0px;")
            scroll_layout.addWidget(section_label)

            tiles_layout = QHBoxLayout()
            tiles_layout.setSpacing(10)

            for plot_info in section_data["plots"]:
                if plot_info["column"] in self.filtered_data.columns:
                    tile = self._create_tile(plot_info, parent_widget)
                    if tile:
                        tiles_layout.addWidget(tile)

            tiles_layout.addStretch()
            tiles_widget = QWidget()
            tiles_widget.setLayout(tiles_layout)
            scroll_layout.addWidget(tiles_widget)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        return scroll_area

    def _create_tile(self, plot_info, parent):
        try:
            fig = create_preview_plot(self.filtered_data, plot_info["column"], plot_info["title"], plot_info["ylabel"])
            tile = Tile(plot_info["title"], parent)
            tile.set_matplotlib_figure(fig)
            tile.clicked.connect(lambda pi=plot_info: self._open_interactive_plot(pi))
            return tile
        except Exception as e:
            print(f"Error creating tile for {plot_info['title']}: {e}")
            return None

    def _open_interactive_plot(self, plot_info):
        if self.filtered_data is not None:
            window = PlotWindow(self.filtered_data, plot_info)
            window.exec()

    def get_data_info(self):
        if self.current_data is None:
            return "No data loaded", "0", "0"
        last_epoch = self.current_data['epoch_utc'].max().strftime('%Y-%m-%d %H:%M:%S')
        total_tles = str(len(self.current_data))
        filtered_tles = str(len(self.filtered_data)) if self.filtered_data is not None else "0"
        return last_epoch, filtered_tles, total_tles