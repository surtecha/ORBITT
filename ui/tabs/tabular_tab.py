from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt


def create_tabular_widget(dataframe):
    column_headers = {
        'time': 'Epoch',
        'a': 'Semi Major Axis (km)',
        'e': 'Eccentricity',
        'i': 'Inclination (deg)',
        'raan': 'RAAN (deg)',
        'aop': 'Arg of Perigee (deg)',
        'ma': 'Mean Anomaly (deg)',
        'bstar': 'B-Star',
        'mean_motion': 'Mean Motion (rev/day)',
        'mean_motion_derivative': 'Mean Motion Deriv (rev/day²)',
        'revolution_number': 'Revolution Number'
    }
    
    table = QTableWidget()
    table.setRowCount(len(dataframe))
    table.setColumnCount(len(dataframe.columns))
    
    headers = [column_headers.get(col, col) for col in dataframe.columns]
    table.setHorizontalHeaderLabels(headers)

    for i, row in dataframe.iterrows():
        for j, value in enumerate(row):
            if isinstance(value, (int, float)) and (dataframe.columns[j] != 'time' or dataframe.columns[j] != 'bstar'):
                formatted_value = f"{float(value):.8f}".rstrip('0').rstrip('.')
            else:
                formatted_value = str(value)
            
            item = QTableWidgetItem(formatted_value)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            table.setItem(i, j, item)

    table.resizeColumnsToContents()
    return table
