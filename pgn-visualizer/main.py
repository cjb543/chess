import sys

from pathlib import Path

from PyQt6.QtCore import QSize, Qt

from PyQt6.QtWidgets import (QApplication, QFileDialog, QVBoxLayout,
                             QHBoxLayout, QWidget, QPushButton,
                             QMainWindow)

from initUI import UILayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Program Title
        self.setWindowTitle("PGN Visualizer")

        # Set Program Size to 640x480 fixed
        self.setFixedSize(QSize(640,480))

        # Initialize Layout
        ui_layout = UILayout()
        self.setCentralWidget(ui_layout)


# Execute program
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()