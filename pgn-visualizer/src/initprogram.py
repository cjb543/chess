from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QPushButton, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence
from pathlib import Path
from board import ChessBoard
from processing import is_valid_pgn

main_window = None

class initProgram(QWidget):
    def __init__(self):
        super().__init__()

        global main_window
        main_window = self

        # Connect Board, Import PGN, and Navigation Arrows
        boardUploadArrows = QVBoxLayout()

        # Initialize Chess Board and add to layout
        self.board_widget = ChessBoard()
        self.board_widget.setFixedSize(self.board_widget.board_size, self.board_widget.board_size)
        ChessBoard.construct_board(self.board_widget)
        boardUploadArrows.addWidget(self.board_widget, 0, Qt.AlignmentFlag.AlignCenter)

        # Initialize Upload Button and add to layout
        upload_button = QPushButton("Import PGN")
        upload_button.isCheckable = True
        upload_button.clicked.connect(self.upload_file)
        boardUploadArrows.addWidget(upload_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Connect Navigation Arrows via Sub-Layout
        arrow_buttons = QHBoxLayout()

        # Initialize Previous Move Arrow Key and add to sub-layout
        previous_move_button = QPushButton("<-")
        previous_move_button.isCheckable = True
        self.prevMoveShortcut = QShortcut(QKeySequence('Left'), self)
        self.prevMoveShortcut.activated.connect(ChessBoard.previousMove_static)
        previous_move_button.clicked.connect(ChessBoard.previousMove_static)
        arrow_buttons.addWidget(previous_move_button,  0, Qt.AlignmentFlag.AlignRight)
        
        # Initialize Next Move Arrow Key and add to sub-layout
        next_move_button = QPushButton("->")
        next_move_button.isCheckable = True
        self.nextMoveShortcut = QShortcut(QKeySequence('Right'), self)
        self.nextMoveShortcut.activated.connect(ChessBoard.nextMove_static)
        next_move_button.clicked.connect(ChessBoard.nextMove_static)
        arrow_buttons.addWidget(next_move_button, 0, Qt.AlignmentFlag.AlignLeft)

        # Add both arrows to layout
        boardUploadArrows.addLayout(arrow_buttons)

        # Connect all right side bar info
        rightSideInfo = QVBoxLayout()

        # Set label defaults
        whitevsblack_label = QLabel("Names: N/A")
        elocounts_label = QLabel("Elos: N/A")
        date_label = QLabel("Date: N/A")
        event_label = QLabel("Event: N/A")
        movecount_label = QLabel("Turn: N/A")
        winner_label = QLabel("Winner: N/A")

        whitevsblack_label.setWordWrap(True)  # Add word wrap for long names
        event_label.setWordWrap(True)  # Add word wrap for long names

        # Add widgets to the main rightSideInfo layout
        rightSideInfo.addWidget(whitevsblack_label, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.addWidget(elocounts_label, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.addWidget(date_label, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.addWidget(event_label, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.addWidget(movecount_label, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.addWidget(winner_label, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.setContentsMargins(20,0,0,30)

        # Throw all together
        complete_layout = QHBoxLayout()
        complete_layout.addLayout(boardUploadArrows)
        complete_layout.addLayout(rightSideInfo)
        widget = QWidget()
        widget.setLayout(complete_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(widget)


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