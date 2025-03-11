from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QPushButton, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence, QKeyEvent
from pathlib import Path
import re

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
        upload_button.clicked.connect(self.uploadFile)
        
        # Initialize Turn Arrows
        next_move_button = QPushButton("->")
        next_move_button.isCheckable = True
        next_move_button.clicked.connect(processing.nextMove)
        previous_move_button = QPushButton("<-")
        previous_move_button.isCheckable = True
        previous_move_button.clicked.connect(processing.previousMove)

        # Initialize Hotkeys
        self.nextMoveShortcut = QShortcut(QKeySequence('Right'), self)
        self.nextMoveShortcut.activated.connect(processing.nextMove)
        
        self.prevMoveShortcut = QShortcut(QKeySequence('Left'), self)
        self.prevMoveShortcut.activated.connect(processing.previousMove)

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

    # When user clicks "Import PGN" and attempts to upload a PGN file
    def uploadFile(self):
        documents_dir = str(Path.home() / "Documents")
        fname = QFileDialog.getOpenFileName(
            self, 
            'Open PGN File', 
            documents_dir, 
            'Text Files (*.txt);;All Files (*)'
        )
        if fname[0]:
            self.loadFile(fname[0])

    # Error checking and processing of uploaded PGN file
    def loadFile(self, filepath):
        try:
            # Check validity of file extension (.txt/.pgn), erroring if incorrect
            file_extension = Path(filepath).suffix.lower()
            if file_extension not in ['.pgn', '.txt']:
                QMessageBox.warning(self, "Invalid File", "Please select a .pgn or .txt file")
                return
            
            # Read file into variable
            with open(filepath, 'r') as file:
                pgn_content = file.read()

            # If the PGN file is correctly formatted, process it for rendering
            if self.isValidPGN(pgn_content):
                processing.processPGN(pgn_content)
            
            # Error if .pgn or .txt has invalid PGN formatting
            else:
                QMessageBox.warning(self, "Invalid PGN", "The file does not contain valid PGN notation")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading file: {e}")
    
    def isValidPGN(self, content):
        # Check if file has all valid tags
        required_tags = ['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result']
        for tag in required_tags:
            if f"[{tag} " not in content:
                return False

        # Use regex to check for valid moves (doesn't check legality of said moves.)
        # Moves are assumed to be legal
        if not re.search(r'\]\s*\n\s*\n', content):
            return False
        
        # If all is well, return true
        return True