from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
import sys
from board import ChessBoard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Program Title
        self.setWindowTitle("PGN Visualizer")

        # Set Program Size to 640x480 fixed
        self.setFixedSize(QSize(640,480))

        # Initialize and show Chess Board
        self.board = ChessBoard()
        self.setCentralWidget(self.board)

        # Initialize Upload Button
        upload_button = QPushButton("Upload")

        # Initialize Next Move Arrow
        next_move_button = QPushButton("Next Move")
        next_move_button.isCheckable = True
        next_move_button.clicked.connect(self.nextMove)

        # Initialize Previous Move Arrow
        previous_move_button = QPushButton("Previous Move")
        previous_move_button.isCheckable = True
        previous_move_button.clicked.connect(self.previousMove)

    def nextMove(self):
        print("Next Move Clicked!")

    def previousMove(self):
        print("Previous Move Clicked!")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()