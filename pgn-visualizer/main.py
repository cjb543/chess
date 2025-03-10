import sys

from pathlib import Path

from PyQt6.QtCore import QSize, Qt

from PyQt6.QtWidgets import (QApplication, QFileDialog, QVBoxLayout,
                             QHBoxLayout, QWidget, QPushButton,
                             QMainWindow)

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
        self.board_widget.setFixedSize(self.board_widget.board_size, self.board_widget.board_size)

        # Initialize Upload Button
        upload_button = QPushButton("Import PGN")
        upload_button.setFixedSize(128,40)
        upload_button.isCheckable = True
        upload_button.clicked.connect(self.uploadFile)
        
        # Initialize Turn Arrows
        next_move_button = QPushButton("->")
        next_move_button.isCheckable = True
        next_move_button.clicked.connect(self.nextMove)
        previous_move_button = QPushButton("<-")
        previous_move_button.isCheckable = True
        previous_move_button.clicked.connect(self.previousMove)

        # General Layout Properties
        complete_layout = QVBoxLayout()
        complete_layout.setSpacing(8)

        # Add Chess Board and Upload Button to Layout
        complete_layout.addWidget(self.board_widget, 0, Qt.AlignmentFlag.AlignCenter)
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

    # Show next board position
    def nextMove(self):
        print("Next Move Clicked!")

    # Show previous board position
    def previousMove(self):
        print("Previous Move Clicked!")

    # Open file dialog after clicking "Import PGN"
    def uploadFile(self):
        documents_dir = str(Path.home() / "Documents")
        fname = QFileDialog.getOpenFileName(self, 'Open file', documents_dir)
        if fname[0]:
            self.loadFile(fname[0])

    # Error checking and processing of uploaded PGN file
    def loadFile(self, filepath):
        try:
            with open(filepath, 'r') as file:
                # Process
                pass
        except Exception as e:
            print(f"Error loading file: {e}")

# Execute program
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()