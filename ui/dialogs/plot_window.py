import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns


class PlotWindow:
    def __init__(self, data, plot_info, parent=None):
        self.data = data.copy()
        self.plot_info = plot_info
        self.create_interactive_plot()

    def create_interactive_plot(self):
        if len(self.data) == 0:
            return

        self.data['epoch_utc'] = pd.to_datetime(self.data['epoch_utc'])
        self.data = self.data.sort_values('epoch_utc')
        y_column = self.plot_info['column']

        if y_column not in self.data.columns:
            return

        valid_data = self.data.dropna(subset=['epoch_utc', y_column])
        if len(valid_data) == 0:
            return

        sns.set_style("whitegrid")
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.canvas.manager.set_window_title(self.plot_info['title'])

        timestamps = valid_data['epoch_utc']
        y_values = valid_data[y_column].astype(float)

        line = ax.plot(timestamps, y_values, color='#1f77b4', linewidth=2.5,
                       marker='o', markersize=5, alpha=0.8, markerfacecolor='white',
                       markeredgecolor='#1f77b4', markeredgewidth=2, label=self.plot_info['title'])[0]

        self._add_hover_functionality(fig, ax, line, timestamps, y_values)

        ax.set_xlabel('Time', fontsize=13, fontweight='600', color='#2c3e50')
        ax.set_ylabel(self.plot_info['ylabel'], fontsize=13, fontweight='600', color='#2c3e50')
        ax.set_title(f"{self.plot_info['title']}", fontsize=16, fontweight='700',
                     pad=25, color='#2c3e50')

        ax.tick_params(axis='both', which='major', labelsize=11, colors='#34495e')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#bdc3c7')
        ax.spines['bottom'].set_color('#bdc3c7')

        ax.xaxis.set_major_formatter(DateFormatter('%m/%d %H:%M'))
        time_range = (timestamps.max() - timestamps.min()).total_seconds()

        if time_range <= 86400:
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=max(1, int(time_range / 3600 / 8))))
        elif time_range <= 604800:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        elif time_range <= 2592000:
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, int(time_range / 86400 / 10))))
        else:
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=max(1, int(time_range / 604800 / 10))))

        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.15)
        plt.show()

    def _add_hover_functionality(self, fig, ax, line, timestamps, y_values):
        annot = ax.annotate('', xy=(0, 0), xytext=(15, 15), textcoords="offset points",
                            bbox=dict(boxstyle="round,pad=0.5", facecolor="#ecf0f1", alpha=0.95,
                                      edgecolor="#34495e", linewidth=1),
                            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.1",
                                            color="#34495e", lw=1.5),
                            fontsize=10, ha='left', color='#2c3e50')
        annot.set_visible(False)

        def on_hover(event):
            if event.inaxes == ax:
                x_data = mdates.date2num(timestamps)
                y_data = y_values.values

                if len(x_data) > 0:
                    distances = np.sqrt((x_data - event.xdata) ** 2 +
                                        ((y_data - event.ydata) / (ax.get_ylim()[1] - ax.get_ylim()[0])) ** 2)
                    min_dist_idx = np.argmin(distances)

                    if distances[min_dist_idx] < 0.1:
                        x_val = timestamps.iloc[min_dist_idx]
                        y_val = y_data[min_dist_idx]
                        hover_text = f"Time: {x_val.strftime('%Y-%m-%d %H:%M:%S')}\n{self.plot_info['ylabel']}: {y_val:.6f}"
                        annot.xy = (x_data[min_dist_idx], y_val)
                        annot.set_text(hover_text)
                        annot.set_visible(True)
                        fig.canvas.draw_idle()
                        return

                if annot.get_visible():
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', on_hover)


def create_interactive_plot(data, plot_info):
    PlotWindow(data, plot_info)