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
        processing.set_board(self.board_widget)
        upload_button = QPushButton("Import PGN")
        upload_button.setFixedSize(128,40)
        upload_button.isCheckable = True
        upload_button.clicked.connect(self.uploadFile)
        next_move_button = QPushButton("->")
        next_move_button.isCheckable = True
        next_move_button.clicked.connect(processing.nextMove)
        previous_move_button = QPushButton("<-")
        previous_move_button.isCheckable = True
        previous_move_button.clicked.connect(processing.previousMove)
        self.nextMoveShortcut = QShortcut(QKeySequence('Right'), self)
        self.nextMoveShortcut.activated.connect(processing.nextMove)
        self.prevMoveShortcut = QShortcut(QKeySequence('Left'), self)
        self.prevMoveShortcut.activated.connect(processing.previousMove)
        complete_layout = QVBoxLayout()
        complete_layout.setSpacing(8)
        complete_layout.addWidget(self.board_widget, 0, Qt.AlignmentFlag.AlignCenter)
        complete_layout.addWidget(upload_button, 0, Qt.AlignmentFlag.AlignCenter)
        arrow_buttons = QHBoxLayout()
        arrow_buttons.addWidget(previous_move_button,  0, Qt.AlignmentFlag.AlignRight)
        arrow_buttons.addWidget(next_move_button, 0, Qt.AlignmentFlag.AlignLeft)
        complete_layout.addLayout(arrow_buttons)
        self.setLayout(complete_layout)

    def uploadFile(self):
        documents_dir = str(Path.home() / "Documents")
        fname = QFileDialog.getOpenFileName(
            self, 
            'Open PGN File', 
            documents_dir, 
            'Text Files (*.txt);;PGN Files (*.pgn);;All Files (*)'
        )
        if fname[0]:
            self.loadFile(fname[0])

    def loadFile(self, filepath):
        try:
            file_extension = Path(filepath).suffix.lower()
            if file_extension not in ['.pgn', '.txt']:
                QMessageBox.warning(self, "Invalid File", "Please select a .pgn or .txt file")
                return
            with open(filepath, 'r') as file:
                pgn_content = file.read()
            if self.isValidPGN(pgn_content):
                processing.processPGN(pgn_content)
            else:
                QMessageBox.warning(self, "Invalid PGN", "The file does not contain valid PGN notation")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading file: {e}")
    
    def isValidPGN(self, content):
        if not re.search(r'\[.+\]', content):
            return False
        if not re.search(r'\d+\.', content):
            return False

        return True