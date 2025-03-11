import sys
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (QApplication, QMainWindow)
from PyQt6.QtGui import QIcon
from initUI import UILayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window Title, Size, and Icon
        self.setWindowTitle("PGN Visualizer")
        self.setFixedSize(QSize(640,480))
        self.setWindowIcon(QIcon('./assets/favicon.png'))

        import ctypes                                                          # I
        myappid = 'cjb543.pgnvisualizer.pgn.000'                               # Love
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid) # Windows!

        ui_layout = UILayout()
        self.setCentralWidget(ui_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()