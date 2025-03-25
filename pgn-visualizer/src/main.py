import sys, ctypes
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar
from PyQt6.QtGui import QIcon, QAction
from initprogram import initProgram

# Create toolbar and menus
def create_menus(main_window):
    # Main toolbar
    menu_bar = main_window.menuBar()

    # "File"
    file_menu = menu_bar.addMenu('&File')

    # "Open PGN..."
    open_PGN = QAction(QIcon('./assets/open.png'), '&Open PGN...', main_window)
    open_PGN.triggered.connect(initProgram.upload_file_static)
    open_PGN.setStatusTip('Open a PGN File')
    open_PGN.setShortcut('Ctrl+O')
    file_menu.addAction(open_PGN)

    # "Settings"
    settings_menu = menu_bar.addMenu('&Settings')
    change_mode = QAction(QIcon('./assets/change_mode.png'), '&Switch Theme (Light/Dark)', main_window)
    change_mode.triggered.connect(initProgram.change_window_theme)
    change_mode.setStatusTip("Switch to and from light mode")
    change_mode.setShortcut('Ctrl+M')
    settings_menu.addAction(change_mode)

    # "Help"
    help_menu = menu_bar.addMenu('&Help')
    what_is_PGN = QAction(QIcon('./assets/help.png'), '&What is PGN?', main_window)
    what_is_PGN.triggered.connect(initProgram.help_user)
    help_menu.setStatusTip("Learn how to use this program")
    help_menu.addAction(what_is_PGN)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window Title, Size, and Icon
        self.setWindowTitle("Chess Visualizer")
        self.setWindowIcon(QIcon('./favicon.png'))
        self.setMinimumSize(640,480)

        # Set Window ID (Needed for taskbar icon)
        myappid = 'cjb543.pgnvisualizer.pgn.000'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Start Program
        program = initProgram()
        self.setCentralWidget(program)

        create_menus(self)
        

# If ran directly, start and show program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Windows') # Dark mode enabling

    # Set App Styles
    with open("./styles.qss", 'r') as f:
        style = f.read()
        app.setStyleSheet(style)
        
    window = MainWindow()
    window.show()
    app.exec()