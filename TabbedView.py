import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QStackedWidget
)
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
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
        tab_names = ["Tab 1", "Tab 2", "Tab 3"]

        for i, name in enumerate(tab_names):
            # Create and style buttons
            btn = QPushButton(name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda _, index=i: self.switch_tab(index))
            self.tab_buttons.addWidget(btn)
            self.tabs.append(btn)

            # Create views
            page = QWidget()
            page_layout = QVBoxLayout(page)
            page_layout.addWidget(QLabel(f"Content for {name}", alignment=Qt.AlignCenter))
            self.stack.addWidget(page)

        # Select the first tab by default
        self.switch_tab(0)

    def switch_tab(self, index):
        for i, btn in enumerate(self.tabs):
            btn.setChecked(i == index)
        self.stack.setCurrentIndex(index)


# Run the app
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
