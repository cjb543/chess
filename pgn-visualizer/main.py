from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMainWindow
import sys
from board import ChessBoard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Program Title
        self.setWindowTitle("PGN Visualizer")

        # Set Program Size to 640x480 fixed
        self.setFixedSize(QSize(640,480))

        # Initialize Chess Board
        self.board_widget = ChessBoard()
        self.board_widget.setFixedSize(QSize(640, 360))

        # Initialize Upload Button
        upload_button = QPushButton("Upload")
        upload_button.setFixedHeight(40)
        upload_button.isCheckable = True
        upload_button.clicked.connect(self.uploadFile)
        
        # Initialize Next Move Arrow
        next_move_button = QPushButton("->")
        next_move_button.isCheckable = True
        next_move_button.clicked.connect(self.nextMove)

        # Initialize Previous Move Arrow
        previous_move_button = QPushButton("<-")
        previous_move_button.isCheckable = True
        previous_move_button.clicked.connect(self.previousMove)

        # General Layout Properties
        complete_layout = QVBoxLayout()
        complete_layout.setSpacing(8)

        # Add Chess Board to Layout
        complete_layout.addWidget(self.board_widget)
        complete_layout.addWidget(upload_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Add Arrow Buttons to Layout
        arrow_buttons = QHBoxLayout()
        arrow_buttons.addWidget(previous_move_button,  0, Qt.AlignmentFlag.AlignRight)
        arrow_buttons.addWidget(next_move_button, 0, Qt.AlignmentFlag.AlignLeft)
        complete_layout.addLayout(arrow_buttons)

        # Set entire layout as a widget and center
        widget = QWidget()
        widget.setLayout(complete_layout)
        self.setCentralWidget(widget)

    # Function to determine next board position
    def nextMove(self):
        print("Next Move Clicked!")

    # Function to determine previous board position
    def previousMove(self):
        print("Previous Move Clicked!")

    def uploadFile(self):
        print("Upload Button Clicked!")

# Execute program
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()