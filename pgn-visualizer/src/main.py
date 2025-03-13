import sys
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from initprogram import initProgram

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window Title, Size, and Icon
        self.setWindowTitle("PGN Visualizer")
        self.setFixedSize(QSize(640,480))
        self.setWindowIcon(QIcon('../favicon.png'))

        # Set Window ID (Needed for taskbar icon)
        import ctypes
        myappid = 'cjb543.pgnvisualizer.pgn.000'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Start Program
        program = initProgram()
        self.setCentralWidget(program)

# If ran directly, start and show program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Windows') # Dark mode enabling
    window = MainWindow()
    window.show()
    app.exec()