from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

# board.py
from board import ChessBoard

# processing.py (not a class)
import processing

class UILayout(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Chess Board
        self.board_widget = ChessBoard()
        self.board_widget.setFixedSize(self.board_widget.board_size, self.board_widget.board_size)

        # Initialize Upload Button
        upload_button = QPushButton("Import PGN")
        upload_button.setFixedSize(128,40)
        upload_button.isCheckable = True
        upload_button.clicked.connect(processing.uploadFile)
        
        # Initialize Turn Arrows
        next_move_button = QPushButton("->")
        next_move_button.isCheckable = True
        next_move_button.clicked.connect(processing.nextMove)
        previous_move_button = QPushButton("<-")
        previous_move_button.isCheckable = True
        previous_move_button.clicked.connect(processing.previousMove)

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
        self.setLayout(complete_layout)

