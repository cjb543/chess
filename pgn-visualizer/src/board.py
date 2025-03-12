from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPixmap
from PyQt6.QtCore import Qt
import re, os, sys, processing

board_widget = None

class ChessBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.square_size = 40
        self.board_size = self.square_size * 8
        self.setMinimumSize(200, 200)
        self.pieces = {}
        self.piece_images = {}
        self.setupStartingPosition()
        self.loadPieceImages()
        self.current_position = {}
        self.positions_history = []
        self.current_move_index = -1
    

    # Render board
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        start_x = (self.width() - self.board_size) // 2
        start_y = (self.height() - self.board_size) // 2
        for row in range(8):
            for col in range(8):
                x = start_x + col * self.square_size
                y = start_y + row * self.square_size
                if (row + col) % 2 == 0:
                    color = QColor(240, 217, 181)
                else:
                    color = QColor(181, 136, 99)
                painter.fillRect(x, y, self.square_size, self.square_size, color)
        display_position = self.getCurrentPosition()
        for (row, col), piece_type in display_position.items():
            if piece_type in self.piece_images:
                pixmap = self.piece_images[piece_type]
                if not pixmap.isNull():
                    x = start_x + col * self.square_size
                    y = start_y + row * self.square_size
                    offset_x = (self.square_size - pixmap.width()) // 2
                    offset_y = (self.square_size - pixmap.height()) // 2
                    painter.drawPixmap(x + offset_x, y + offset_y, pixmap)


    # Initialize board_widget
    def construct_board(board):
        global board_widget
        board_widget = board
    

    # Initialize starting board position
    def setupStartingPosition(self):
        self.pieces = {}
        for col in range(8):
            self.pieces[(1, col)] = "bP"
            self.pieces[(6, col)] = "wP"
        back_row_pieces = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for col in range(8):
            self.pieces[(0, col)] = "b" + back_row_pieces[col]
            self.pieces[(7, col)] = "w" + back_row_pieces[col]
        self.positions_history = []
        self.current_move_index = -1
    

    # Load pieces for all cases
    def loadPieceImages(self):
        import os
        import sys
        def get_base_path():
            if getattr(sys, 'frozen', False):
                return sys._MEIPASS
            else:
                return os.path.dirname(os.path.abspath(__file__))
            
        # Load all images
        piece_types = [
            "wP", "wR", "wN", "wB", "wQ", "wK",
            "bP", "bR", "bN", "bB", "bQ", "bK"
        ]
        base_path = get_base_path()
        for piece_type in piece_types:
            possible_paths = [
                os.path.join(base_path, f"{piece_type}.png"),
                os.path.join(os.path.dirname(base_path), f"{piece_type}.png"),
                f"assets/{piece_type}.png",
                f"{piece_type}.png"
            ]
            pixmap = None
            loaded_path = None
            for path in possible_paths:
                temp_pixmap = QPixmap(path)
                if not temp_pixmap.isNull():
                    pixmap = temp_pixmap
                    loaded_path = path
                    break
            if pixmap:
                pixmap = pixmap.scaled(
                    self.square_size,
                    self.square_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            self.piece_images[piece_type] = pixmap


    def getCurrentPosition(self):
        if self.current_move_index == -1:
            return self.pieces
        elif 0 <= self.current_move_index < len(self.positions_history):
            return self.positions_history[self.current_move_index]
        return self.pieces


    # Replace the PGN parsing method with a call to the processing module
    def parsePGN(self, pgn_content):
        processing.parse_pgn(pgn_content, self)
        self.update()
    

    # Update board instance to next move
    def nextMove(self):
        if self.current_move_index < len(self.positions_history) - 1:
            self.current_move_index += 1
            self.update()
            return True
        return False
    

    # Update board instance to previous move
    def previousMove(self):
        if self.current_move_index >= 0:
            self.current_move_index -= 1
            self.update()
            return True
        return False
    
    # Reset game to first position (not currently used)
    def resetToStart(self):
        self.current_move_index = -1
        self.update()
    

    # Static next move method that connects to onscreen UI button
    @classmethod
    def nextMove_static(cls):
        global board_widget
        if board_widget:
            return board_widget.nextMove()
        return False
    

    # Static previous move method that connects to onscreen UI button
    @classmethod
    def previousMove_static(cls):
        global board_widget
        if board_widget:
            return board_widget.previousMove()
        return False
    

    # Static call to process PGN file
    @classmethod
    def process_pgn(cls, pgn_content):
        global board_widget
        if board_widget:
            board_widget.parsePGN(pgn_content)
            board_widget.resetToStart()