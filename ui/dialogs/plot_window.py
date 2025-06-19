from PySide6.QtWidgets import QDialog, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtWebEngineWidgets import QWebEngineView
import plotly.graph_objects as go
import plotly.offline as pyo
import pandas as pd
import tempfile
import os


class PlotWindow(QDialog):
    def __init__(self, data, plot_info, parent=None):
        super().__init__(parent)
        self.data = data.copy()
        self.plot_info = plot_info
        self.setModal(False)
        self.setup_ui()
        self.create_plot()

    def setup_ui(self):
        self.setWindowTitle(f"Interactive Plot - {self.plot_info['title']}")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowFlags(Qt.WindowType.Window)

        layout = QVBoxLayout(self)

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

    def create_plot(self):
        if len(self.data) == 0:
            return

        self.data['epoch_utc'] = pd.to_datetime(self.data['epoch_utc'])
        self.data = self.data.sort_values('epoch_utc')

        epoch_column = 'epoch_utc'
        y_column = self.plot_info['column']

        if y_column not in self.data.columns:
            return

        valid_data = self.data.dropna(subset=[epoch_column, y_column])

        if len(valid_data) == 0:
            return

        timestamps = valid_data[epoch_column]
        y_values = valid_data[y_column].astype(float)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=timestamps,
            y=y_values,
            mode='lines+markers',
            name=self.plot_info['title'],
            line=dict(color='#3498db', width=2.5),
            marker=dict(
                color='#2980b9',
                size=5,
                opacity=0.8,
                symbol='circle',
                line=dict(width=1, color='#ffffff')
            ),
            hovertemplate='<b>Time</b>: %{x}<br><b>' + self.plot_info['ylabel'] + '</b>: %{y:.6f}<extra></extra>'
        ))

        fig.update_layout(
            xaxis=dict(
                title=dict(text='Time', font=dict(size=14, color='#2c3e50')),
                showgrid=True,
                gridcolor='rgba(52, 73, 94, 0.15)',
                gridwidth=1,
                tickformat='%m/%d %H:%M',
                tickfont=dict(size=12, color='#34495e'),
                linecolor='#bdc3c7',
                linewidth=1
            ),
            yaxis=dict(
                title=dict(text=self.plot_info['ylabel'], font=dict(size=14, color='#2c3e50')),
                showgrid=True,
                gridcolor='rgba(52, 73, 94, 0.15)',
                gridwidth=1,
                tickfont=dict(size=12, color='#34495e'),
                linecolor='#bdc3c7',
                linewidth=1
            ),
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='#ffffff',
            hovermode='x unified',
            showlegend=False,
            margin=dict(l=70, r=30, t=30, b=60),
            autosize=True,
            height=None,
            dragmode='pan',
            font=dict(family='Segoe UI, Arial, sans-serif', color='#2c3e50')
        )

        fig.update_xaxes(rangeslider_visible=False)

        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
        html_content = pyo.plot(fig, output_type='div', include_plotlyjs=True)

        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Interactive Plot</title>
            <style>
                body {{ 
                    margin: 0; 
                    padding: 0; 
                    height: 100vh; 
                    overflow: hidden; 
                    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                    font-family: 'Segoe UI', Arial, sans-serif;
                }}
                .plotly-graph-div {{ 
                    height: 100vh !important; 
                    width: 100% !important; 
                    box-shadow: inset 0 1px 3px rgba(0,0,0,0.12);
                }}
                .modebar {{
                    background: rgba(255,255,255,0.9) !important;
                    border-radius: 4px !important;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
                }}
                .modebar-btn {{
                    color: #34495e !important;
                }}
                .modebar-btn:hover {{
                    background: rgba(52, 152, 219, 0.1) !important;
                }}
            </style>
            <script>
                window.addEventListener('load', function() {{
                    var plotDiv = document.querySelector('.plotly-graph-div');
                    if (plotDiv && plotDiv._fullLayout) {{
                        plotDiv.on('plotly_relayout', function(eventdata) {{
                            if (eventdata['xaxis.range[0]'] || eventdata['yaxis.range[0]']) {{
                                // Handle zoom/pan events if needed
                            }}
                        }});
                    }}
                }});
            </script>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        temp_file.write(full_html)
        temp_file.close()

        self.web_view.load(f"file://{temp_file.name}")
        self.temp_file_path = temp_file.name

    def closeEvent(self, event):
        if hasattr(self, 'temp_file_path') and os.path.exists(self.temp_file_path):
            try:
                os.unlink(self.temp_file_path)
            except:
                pass
        super().closeEvent(event)