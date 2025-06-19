import sys, json, os

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QStackedWidget, QSizePolicy, QTableView, QTabWidget,
    QMessageBox, QListWidgetItem
)

from PyQt5.QtCore import Qt, QAbstractTableModel

import gc_ohcl, gekurl
from PandasModels import *

class SelectionWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout
        self.main_layout = QVBoxLayout(self)

        # Get coins list
        if not os.path.exists('./api_data/coins_list.json'):
            gekurl.call_api_get('https://api.coingecko.com/api/v3/coins/list', 'coins_list.json')

        # Title at the top, centered
        self.selected_coin = gc_ohcl.cr_coin.id
        self.path = './api_data/coins_list.json'
        self.title = QLabel(f"Selected Coin: {self.selected_coin.title()}")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.main_layout.addWidget(self.title)

        self.center_hbox_layout = QHBoxLayout()

        # List of strings
        self.left_list_layout = QVBoxLayout()
        self.list_widget = QListWidget()

        self.left_list_layout.addWidget(self.list_widget)

        # Selected item description
        self.right_description_layout = QVBoxLayout()
        self.name_label = QLabel("Select an ID")
        self.name_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.desc_label = QLabel("")
        self.desc_label.setWordWrap(True)
        self.right_description_layout.addWidget(self.name_label)
        self.right_description_layout.addWidget(self.desc_label)

        self.center_hbox_layout.addLayout(self.left_list_layout)
        self.center_hbox_layout.addLayout(self.right_description_layout)

        self.main_layout.addLayout(self.center_hbox_layout)

        self.load_data(self.path)

        self.list_widget.itemSelectionChanged.connect(self.display_details)

        # "Choose" button
        choose_button = QPushButton("Choose")
        choose_button.clicked.connect(self.on_choose)
        self.main_layout.addWidget(choose_button)

    def load_data(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        for entry in self.data:
            item = QListWidgetItem(entry["id"])
            # Store full object in item data
            item.setData(Qt.UserRole, entry)
            self.list_widget.addItem(item)

    def display_details(self):
        selected = self.list_widget.currentItem()
        if selected:
            data = selected.data(Qt.UserRole)
            self.name_label.setText(data["name"])
            self.desc_label.setText(data.get("description", "(no description)"))

    def on_choose(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            choice = selected_items[0].text()
            self.selected_coin = choice
            self.title.setText(f"Selected Coin: {self.selected_coin.title()}")
            gc_ohcl.cr_coin.set_id(self.selected_coin)
            gc_ohcl.cr_coin.refresh()
            df = gc_ohcl.cr_coin.get_data_frame()

            model.setDataFrame(df)
            #QMessageBox.information(self, "You chose", f"You selected: {choice}")
        else:
            pass
            #QMessageBox.warning(self, "No selection", "Please select an option.")

class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabbed View with Buttons")
        self.resize(600, 400)

        # Main layout
        layout = QVBoxLayout(self)

        # Tab buttons (top)
        self.tab_buttons = QHBoxLayout()
        layout.addLayout(self.tab_buttons)

        # Stack widget (central content)
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # Create tabs and views
        self.tabs = []
        tab_names = ["Main", "Market", "OHCL"]

        for i, name in enumerate(tab_names):
            # Create and style buttons
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, index=i: self.switch_tab(index))
            self.tab_buttons.addWidget(btn)
            self.tabs.append(btn)

            match(name):
                case "Main":
                    page = QWidget()
                    page_layout = QVBoxLayout(page)
                    selection_widget = SelectionWidget()
                    self.stack.addWidget(selection_widget)
                case "Market":
                    page = QWidget()
                    page_layout = QVBoxLayout(page)
                    label = QLabel(f"Not implemented yet...", alignment=Qt.AlignCenter)
                    label.setStyleSheet("font-size: 20px; font-weight: bold;")
                    page_layout.addWidget(label)
                    self.stack.addWidget(page)
                case "OHCL":
                    global model
                    view = QTableView()

                    view.setModel(model)
                    self.stack.addWidget(view)

        # Select the first tab by default
        self.switch_tab(0)

    def switch_tab(self, index):
        for i, btn in enumerate(self.tabs):
            btn.setChecked(i == index)
        self.stack.setCurrentIndex(index)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MyCoins - CoinGecko RT-Graph')
        self.setGeometry(300, 300, 800, 600)
        self.setWindowIcon(QIcon('CoinGecko.png'))

df = gc_ohcl.cr_coin.get_data_frame()
model = OHCLModel(df)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    tabWidget = TabWidget()
    selection_widget = SelectionWidget()
    window.setCentralWidget(tabWidget)

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()