import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QAbstractTableModel


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def setDataFrame(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            return str(self._data.iat[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            else:
                return str(self._data.index[section])
        return None


app = QApplication(sys.argv)
window = QMainWindow()

# Initial DataFrame
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Email": ["alice@example.com", "bob@example.com", "charlie@example.com"]
})

model = PandasModel(df)
view = QTableView()
view.setModel(model)

# Button to change DataFrame
button = QPushButton("Load New Data")
def load_new_data():
    new_df = pd.DataFrame({
        "Name": ["Dave", "Eve"],
        "Age": [40, 28],
        "Email": ["dave@example.com", "eve@example.com"]
    })
    model.setDataFrame(new_df)

button.clicked.connect(load_new_data)

# Layout
container = QWidget()
layout = QVBoxLayout(container)
layout.addWidget(view)
layout.addWidget(button)

window.setCentralWidget(container)
window.setWindowTitle("Updatable DataFrame in PyQt5")
window.resize(600, 300)
window.show()

sys.exit(app.exec_())
