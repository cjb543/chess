from PyQt6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, 
                             QMessageBox, QPushButton, QToolBar, QFileDialog,
                             QTextEdit, QLineEdit)
from PyQt6.QtGui import (QShortcut, QKeySequence, QResizeEvent, QFont)
from processing import is_valid_pgn
from PyQt6.QtCore import Qt
from board import ChessBoard
from pathlib import Path

main_window = None

class initProgram(QWidget):
    def __init__(self):
        super().__init__()

        global main_window
        main_window = self

        # Initialize Chess Board
        self.board_widget = ChessBoard()
        self.board_widget.setFixedSize(self.board_widget.board_size, self.board_widget.board_size)
        ChessBoard.construct_board(self.board_widget)

        # Initialize Upload Buttons
        fen_input = QLineEdit("Import FEN String...")
        fen_input.setMaximumHeight(40)
        upload_button = QPushButton("Import PGN")
        upload_button.isCheckable = True
        upload_button.clicked.connect(self.upload_file)

        # Initialize Previous Move Arrow Key
        previous_move_button = QPushButton("<-")
        previous_move_button.isCheckable = True
        self.prevMoveShortcut = QShortcut(QKeySequence('Left'), self)
        self.prevMoveShortcut.activated.connect(ChessBoard.previousMove_static)
        previous_move_button.clicked.connect(ChessBoard.previousMove_static)
        
        # Initialize Next Move Arrow Key
        next_move_button = QPushButton("->")
        next_move_button.isCheckable = True
        self.nextMoveShortcut = QShortcut(QKeySequence('Right'), self)
        self.nextMoveShortcut.activated.connect(ChessBoard.nextMove_static)
        next_move_button.clicked.connect(ChessBoard.nextMove_static)

        # Initialize Last Move Arrow Key
        last_move_button = QPushButton(">>")
        last_move_button.isCheckable = True
        last_move_button.clicked.connect(ChessBoard.last_move_static)

        # Initialize First Move Arrow Key
        first_move_button = QPushButton("<<")
        first_move_button.isCheckable = True
        first_move_button.clicked.connect(ChessBoard.first_move_static)

        # Define non-move information
        whitevsblack_label = QLabel("Names: N/A")
        elocounts_label = QLabel("Elos: N/A")
        date_label = QLabel("Date: N/A")
        event_label = QLabel("Event: N/A")
        movecount_label = QLabel("Turn: N/A")
        winner_label = QLabel("Winner: N/A")
        whitevsblack_label.setWordWrap(True)
        event_label.setWordWrap(True)


    # Resize gui when window is resized TODO ?
    def resizeEvent(self, event: QResizeEvent):
        pass


    # When "Import PGN" is clicked, open file dialog
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
            if is_valid_pgn(pgn_content):
                ChessBoard.process_pgn(pgn_content)
                self.update_labels(ChessBoard.game_info)
            else:
                QMessageBox.warning(self, "Invalid PGN", "The file does not contain valid PGN notation")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading file: {e}")


    def update_labels(self, game_info):
        # Find the labels in the layout
        for i in range(self.findChild(QHBoxLayout).count()):
            layout_item = self.findChild(QHBoxLayout).itemAt(i)
            if isinstance(layout_item.layout(), QVBoxLayout) and layout_item.layout() != self.findChild(QHBoxLayout).itemAt(0).layout():
                right_side_layout = layout_item.layout()

                # Assign labels directly from the layout
                whitevsblack_label = right_side_layout.itemAt(0).widget()
                elocounts_label = right_side_layout.itemAt(1).widget()
                date_label = right_side_layout.itemAt(2).widget()
                event_label = right_side_layout.itemAt(3).widget()
                movecount_label = right_side_layout.itemAt(4).widget()
                winner_label = right_side_layout.itemAt(5).widget()

                # Update the labels
                whitevsblack_label.setText(f"{game_info['white_player']} vs. {game_info['black_player']}")
                elocounts_label.setText(f"Elo: {game_info['white_elo']} vs. {game_info['black_elo']}")
                date_label.setText(f"Date: {game_info['date']}")
                event_label.setText(f"Event: {game_info['event']}")
                movecount_label.setText(f"Turn: 0")
                winner_label.setText(f"Winner: {game_info['winner']}")

                break 

    # Static function to call "upload_file" from the "File" menu item
    @classmethod
    def upload_file_static(cls):
        if main_window:
            cls.upload_file()

    # Static function to change the window to light/dark mode
    @classmethod
    def change_window_theme(cls):
        # Invert all colors of program.
        pass

    @classmethod
    def help_user(cls):
        # Prompt the user to a help page? Open a webpage?
        pass

    @classmethod
    def change_window_mode(cls):
        # Switch the input to a lineEdit for FEN rather than an upload for PGN
        # Or vice versa :D
        pass

    @classmethod
    def import_FEN_string(cls):
        # Call a FEN String to be processed if imported
        pass