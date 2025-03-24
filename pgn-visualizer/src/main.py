import sys, ctypes
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar
from PyQt6.QtGui import QIcon, QAction
from initprogram import initProgram

# TODO:
#   - Better PGN File Error Checking (formatting; extension-checking is perfect)
#   - Better bounds-checking. If a bad file is read, it shouldn't go past x moves etc...
#   - Add window size responsiveness (buttons and board increase in size)
#   - Better text styling

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window Title, Size, and Icon
        self.setWindowTitle("Chess Visualizer")
        self.setWindowIcon(QIcon('./favicon.png'))

        # Set Window ID (Needed for taskbar icon)
        myappid = 'cjb543.pgnvisualizer.pgn.000'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Start Program
        program = initProgram()
        self.setCentralWidget(program)

        # Create ToolBar and subsequent menus
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        settings_menu = menu_bar.addMenu('&Settings')
        open_action = QAction(QIcon('./assets/open.png'), '&Open PGN...', self)
        open_action.triggered.connect(initProgram.upload_file_static)
        open_action.setStatusTip('Open a PGN File')
        open_action.setShortcut('Ctrl+O')
        file_menu.addAction(open_action)


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