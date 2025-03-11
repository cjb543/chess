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
        self.setWindowTitle("PGN Visualizer")
        self.setFixedSize(QSize(640,480))
        self.setWindowIcon(QIcon('./assets/favicon.png'))
        import ctypes
        myappid = 'cjb543.pgnvisualizer.pgn.000'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        ui_layout = UILayout()
        self.setCentralWidget(ui_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()