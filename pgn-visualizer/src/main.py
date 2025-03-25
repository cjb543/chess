import sys, ctypes
from PyQt6.QtWidgets import QApplication, QMainWindow, QToolBar
from PyQt6.QtGui import QIcon, QAction
from initprogram import initProgram

# Create Menus
def create_menus(main_window):
    # Main toolbar
    menu_bar = main_window.menuBar()

    # "File"
    file_menu = menu_bar.addMenu('&File')

    # "File -> Import PGN..."
    import_PGN = QAction(QIcon('./assets/openPGN.png'), '&Import PGN...', main_window)
    import_PGN.triggered.connect(initProgram.upload_file_static)
    import_PGN.setStatusTip('Import a PGN File')
    import_PGN.setShortcut('Ctrl+U')
    file_menu.addAction(import_PGN)

    # "File -> Import FEN..."
    import_FEN = QAction(QIcon('./assets/openFEN.png'), '&Import FEN...', main_window)
    import_FEN.triggered.connect(initProgram.import_FEN_string)
    import_FEN.setStatusTip('Import a FEN String')
    import_FEN.setShortcut('Ctrl+F')
    file_menu.addAction(import_FEN)

    # "Settings"
    settings_menu = menu_bar.addMenu('&Settings')

    # "Settings -> Change Theme"
    change_theme = QAction(QIcon('./assets/change_mode.png'), '&Switch Theme', main_window)
    change_theme.triggered.connect(initProgram.change_window_theme)
    change_theme.setStatusTip("Switch to and from light mode")
    change_theme.setShortcut('Ctrl+T')
    settings_menu.addAction(change_theme)

    # "Settings -> Change Mode"
    change_mode = QAction(QIcon('./assets/change_theme.png'), '&Switch Mode', main_window)
    change_mode.triggered.connect(initProgram.change_window_mode)
    change_mode.setStatusTip("Switch between PGN and FEN")
    change_mode.setShortcut('Ctrl+M')
    settings_menu.addAction(change_mode)

    # "Help"
    help_menu = menu_bar.addMenu('&Help')
    help_menu.setStatusTip("Learn how to use this program")

    # "Help -> What is PGN?"
    what_is_PGN = QAction(QIcon('./assets/what_is_PGN.png'), '&What is PGN?', main_window)
    what_is_PGN.triggered.connect(initProgram.help_user)
    help_menu.addAction(what_is_PGN)

    # "Help -> What is FEN"
    what_is_FEN = QAction(QIcon('./assets/what_is_FEN.png'), '&What is FEN?', main_window)
    what_is_FEN.triggered.connect(initProgram.help_user)
    help_menu.addAction(what_is_FEN)


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