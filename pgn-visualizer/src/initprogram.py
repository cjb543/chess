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

        self.setStyleSheet("""
            background-color: #333333;
            color: #F5F5F5;
        """)

        # Style constants
        LABEL_FONT_SIZE = 10  # Base font size
        HEADER_FONT_SIZE = 12  # Slightly larger for important info
        FONT_FAMILY = "Times"  # Consistent font family
        BACKGROUND_COLOR = 454444

        # Connect Board, Import PGN, and Navigation Arrows
        boardUploadArrows = QVBoxLayout()

        # Initialize Chess Board and add to layout
        self.board_widget = ChessBoard()
        self.board_widget.setFixedSize(self.board_widget.board_size, self.board_widget.board_size)
        ChessBoard.construct_board(self.board_widget)
        boardUploadArrows.addWidget(self.board_widget, 0, Qt.AlignmentFlag.AlignCenter)

        # Initialize Upload Button and add to layout
        upload_button = QPushButton("Import PGN")
        upload_button.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: {LABEL_FONT_SIZE}pt;
            border-radius: 8px;
            background-color: #{BACKGROUND_COLOR}
        """)

        upload_button.setFixedSize(128,30)
        upload_button.isCheckable = True
        upload_button.clicked.connect(self.upload_file)
        boardUploadArrows.addWidget(upload_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Connect Navigation Arrows via Sub-Layout
        arrow_buttons = QHBoxLayout()
        arrow_buttons.setContentsMargins(0,0,0,20)

        # Initialize Previous Move Arrow Key and add to sub-layout
        previous_move_button = QPushButton("<-")
        previous_move_button.setFixedSize(64,30)
        previous_move_button.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: {LABEL_FONT_SIZE}pt;
            border-radius: 8px;
            background-color: #{BACKGROUND_COLOR}
        """)
        previous_move_button.isCheckable = True
        self.prevMoveShortcut = QShortcut(QKeySequence('Left'), self)
        self.prevMoveShortcut.activated.connect(ChessBoard.previousMove_static)
        previous_move_button.clicked.connect(ChessBoard.previousMove_static)
        arrow_buttons.addWidget(previous_move_button,  0, Qt.AlignmentFlag.AlignRight)
        
        # Initialize Next Move Arrow Key and add to sub-layout
        next_move_button = QPushButton("->")
        next_move_button.setFixedSize(64,30)
        next_move_button.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: {LABEL_FONT_SIZE}pt;
            border-radius: 8px;
            background-color: #{BACKGROUND_COLOR}
        """)
        next_move_button.isCheckable = True
        self.nextMoveShortcut = QShortcut(QKeySequence('Right'), self)
        self.nextMoveShortcut.activated.connect(ChessBoard.nextMove_static)
        next_move_button.clicked.connect(ChessBoard.nextMove_static)
        arrow_buttons.addWidget(next_move_button, 0, Qt.AlignmentFlag.AlignLeft)

        # Add both arrows to layout
        boardUploadArrows.addLayout(arrow_buttons)
        boardUploadArrows.setContentsMargins(10,30,10,10)

        # Connect all right side bar info
        rightSideInfo = QVBoxLayout()


        # Apply styles to each label
        date_label = QLabel("Date: N/A")
        date_label.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: {LABEL_FONT_SIZE}pt;
            border-radius: 8px;
        """)

        event_label = QLabel("Event: N/A")
        event_label.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: {LABEL_FONT_SIZE}pt;
            border-radius: 8px;
        """)

        whitevsblack_label = QLabel("Names: N/A")
        whitevsblack_label.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: {HEADER_FONT_SIZE}pt;
            border-radius: 8px;
        """)

        elocounts_label = QLabel("Elos: N/A")
        elocounts_label.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: {LABEL_FONT_SIZE}pt;
            border-radius: 8px;
        """)

        movecount_label = QLabel("Turn: N/A")
        movecount_label.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: {LABEL_FONT_SIZE}pt;
            border-radius: 8px;
        """)

        winner_label = QLabel("Winner: N/A")
        winner_label.setStyleSheet(f"""
            font-family: {FONT_FAMILY};
            font-size: {HEADER_FONT_SIZE}pt;
            border-radius: 8px;
        """)

        # Set fixed sizes for these specific widgets first
        whitevsblack_label.setFixedWidth(180)
        whitevsblack_label.setWordWrap(True)  # Add word wrap for long names
        elocounts_label.setFixedWidth(180)

        # Create a container for the grouped widgets
        grouped_container = QWidget()
        grouped_layout = QVBoxLayout(grouped_container)
        grouped_layout.setContentsMargins(0, 0, 0, 0)

        # Add widgets to the grouped layout
        grouped_layout.addWidget(whitevsblack_label, 0, Qt.AlignmentFlag.AlignCenter)
        grouped_layout.addWidget(elocounts_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Add widgets to the main rightSideInfo layout
        rightSideInfo.addWidget(grouped_container, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.addWidget(date_label, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.addWidget(event_label, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.addWidget(movecount_label, 0, Qt.AlignmentFlag.AlignCenter)
        rightSideInfo.addWidget(winner_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Set fixed sizes for remaining widgets
        date_label.setFixedWidth(180)
        date_label.setFixedHeight(40)
        event_label.setFixedWidth(180)
        event_label.setFixedHeight(40)
        movecount_label.setFixedWidth(180)
        movecount_label.setFixedHeight(40)
        winner_label.setFixedWidth(180)
        winner_label.setFixedHeight(40)

        # Ensure the container has the right size as well
        grouped_container.setFixedWidth(180)
        grouped_container.setFixedHeight(80)

        # Set fixed sizes for all widgets directly in layout3
        for i in range(rightSideInfo.count()):
            widget = rightSideInfo.itemAt(i).widget()
            if widget and widget is not grouped_container:
                widget.setFixedWidth(180)
                widget.setFixedHeight(40)

        # Throw all together
        complete_layout = QHBoxLayout()
        complete_layout.addLayout(boardUploadArrows)
        complete_layout.addLayout(rightSideInfo)  
        widget = QWidget()
        widget.setLayout(complete_layout)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
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
                break
            
        # Update player names and Elos
        grouped_container = right_side_layout.itemAt(0).widget()
        grouped_layout = grouped_container.layout()

        # Update player vs player label
        player_label = grouped_layout.itemAt(0).widget()
        player_label.setText(f"{game_info['white_player']} vs. {game_info['black_player']}")

        # Update Elo label
        elo_label = grouped_layout.itemAt(1).widget()
        elo_label.setText(f"Elo: {game_info['white_elo']} vs. {game_info['black_elo']}")

        # Update date label (index 1 after the grouped container)
        date_label = right_side_layout.itemAt(1).widget()
        date_label.setText(f"Date: {game_info['date']}")

        # Update event label
        event_label = right_side_layout.itemAt(2).widget()
        event_label.setText(f"Event: {game_info['event']}")

        # Skip moves
        movecount_label = right_side_layout.itemAt(3).widget()
        movecount_label.setText(f"Turn: 0")

        # Update winner label
        winner_label = right_side_layout.itemAt(4).widget()
        winner_label.setText(f"Winner: {game_info['winner']}")  