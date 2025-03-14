import sys
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from initprogram import initProgram

# TODO:
#   - Better PGN File Error Checking (formatting; extension-checking is perfect)
#   - Better bounds/error-checking. If a bad file is read, it shouldn't go past x moves etc...
#   - What other functionality can I add?
#       - First Move Button (already coded but not implemented), Last Move Button
#   - Better text styling
#   - Use of a .qss file (Use the entire framework bro)
#   - FEN reader sub program? Switch between the two?

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

    # Set App Styles
    with open("./src/styles.qss", 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
        
    window = MainWindow()
    window.show()
    app.exec()