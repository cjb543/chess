from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QPushButton, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from pathlib import Path
import re
from board import ChessBoard
import processing

class UILayout(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Chess Board
        self.board_widget = ChessBoard()
        self.board_widget.setFixedSize(self.board_widget.board_size, self.board_widget.board_size)
        processing.construct_board(self.board_widget)

        # Initialize Upload Button
        upload_button = QPushButton("Import PGN")
        upload_button.setFixedSize(128,40)
        upload_button.isCheckable = True
        upload_button.clicked.connect(self.upload_file)

        # Initialize Next Move Button
        next_move_button = QPushButton("->")
        next_move_button.isCheckable = True
        next_move_button.clicked.connect(processing.nextMove)
        self.nextMoveShortcut = QShortcut(QKeySequence('Right'), self)
        self.nextMoveShortcut.activated.connect(processing.nextMove)

        # Initialize Previous Move Button
        previous_move_button = QPushButton("<-")
        previous_move_button.isCheckable = True
        previous_move_button.clicked.connect(processing.previousMove)
        self.prevMoveShortcut = QShortcut(QKeySequence('Left'), self)
        self.prevMoveShortcut.activated.connect(processing.previousMove)

        # Initialize board and upload button layout
        complete_layout = QVBoxLayout()
        complete_layout.setSpacing(8)
        complete_layout.addWidget(self.board_widget, 0, Qt.AlignmentFlag.AlignCenter)
        complete_layout.addWidget(upload_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Initialize arrow layout
        arrow_buttons = QHBoxLayout()
        arrow_buttons.addWidget(previous_move_button,  0, Qt.AlignmentFlag.AlignRight)
        arrow_buttons.addWidget(next_move_button, 0, Qt.AlignmentFlag.AlignLeft)

        # Throw it all together
        complete_layout.addLayout(arrow_buttons)
        self.setLayout(complete_layout)

    # When "Import PGN" is clicked
    def upload_file(self):
        documents_dir = str(Path.home() / "Documents")
        fname = QFileDialog.getOpenFileName(
            self, 
            'Open PGN File', 
            documents_dir, 
            'Text Files (*.txt);;PGN Files (*.pgn);;All Files (*)'
        )
        if fname[0]:
            self.load_file(fname[0])

    # Attempts to open the PGN file selected. Checks for file extension and formatting
    def load_file(self, filepath):
        try:
            file_extension = Path(filepath).suffix.lower()
            if file_extension not in ['.pgn', '.txt']:
                QMessageBox.warning(self, "Invalid File", "Please select a .pgn or .txt file")
                return
            with open(filepath, 'r') as file:
                pgn_content = file.read()
            if self.isValidPGN(pgn_content):
                processing.process_pgn(pgn_content)
            else:
                QMessageBox.warning(self, "Invalid PGN", "The file does not contain valid PGN notation")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading file: {e}")
    
    # Checks if a PGN file is valid
    def isValidPGN(self, content):
        if not re.search(r'\[.+\]', content):
            return False
        if not re.search(r'\d+\.', content):
            return False

        return True