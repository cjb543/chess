import sys

from pathlib import Path

from PyQt6.QtCore import QSize, Qt

from PyQt6.QtWidgets import (QApplication, QFileDialog, QVBoxLayout,
                             QHBoxLayout, QWidget, QPushButton,
                             QMainWindow)

from PyQt6.QtGui import QIcon

from initUI import UILayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Program Title
        self.setWindowTitle("PGN Visualizer")

        # Set Program Size to 640x480 fixed
        self.setFixedSize(QSize(640,480))

        # Set Program Icon (when opened)
        self.setWindowIcon(QIcon('./assets/knight.png'))

        # Set Program Icon (taskbar) and set Windows app ID (arbitrary)
        import ctypes
        myappid = 'cjb543.pgnvisualizer.pgn.000' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Initialize Layout
        ui_layout = UILayout()
        self.setCentralWidget(ui_layout)

if __name__ == "__main__":
    # Execute program
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()