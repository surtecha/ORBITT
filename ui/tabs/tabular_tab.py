from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt


def create_tabular_widget(dataframe):
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
    return table
