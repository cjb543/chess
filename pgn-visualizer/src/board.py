from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPixmap
from PyQt6.QtCore import Qt

class ChessBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.square_size = 40
        self.board_size = self.square_size * 8
        self.setMinimumSize(200, 200)
        
        # Initialize dictionaries
        self.pieces = {}
        self.piece_images = {}
        
        # Call setup methods
        self.setupStartingPosition()
        self.loadPieceImages()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        start_x = (self.width() - self.board_size) // 2
        start_y = (self.height() - self.board_size) // 2
        # Board
        for row in range(8):
            for col in range(8):
                x = start_x + col * self.square_size
                y = start_y + row * self.square_size
                if (row + col) % 2 == 0:
                    color = QColor(240, 217, 181)
                else:
                    color = QColor(181, 136, 99)
                painter.fillRect(x, y, self.square_size, self.square_size, color)
        # Pieces
        for (row, col), piece_type in self.pieces.items():
            if piece_type in self.piece_images:
                pixmap = self.piece_images[piece_type]
                if not pixmap.isNull():
                    x = start_x + col * self.square_size
                    y = start_y + row * self.square_size
                   
                    # Center the piece in the square
                    offset_x = (self.square_size - pixmap.width()) // 2
                    offset_y = (self.square_size - pixmap.height()) // 2
                   
                    painter.drawPixmap(x + offset_x, y + offset_y, pixmap)
    
    # Initialize starting position
    def setupStartingPosition(self):
        self.pieces = {}
        for col in range(8):
            self.pieces[(1, col)] = "bP"
            self.pieces[(6, col)] = "wP"
        back_row_pieces = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for col in range(8):
            self.pieces[(0, col)] = "b" + back_row_pieces[col]
            self.pieces[(7, col)] = "w" + back_row_pieces[col]
    
    # Render images in place of established starting position  
    def loadPieceImages(self):
        piece_types = [
            "wP", "wR", "wN", "wB", "wQ", "wK",
            "bP", "bR", "bN", "bB", "bQ", "bK"
        ]
        for piece_type in piece_types:
            image_path = f"assets/{piece_type}.png"
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    self.square_size,
                    self.square_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            self.piece_images[piece_type] = pixmap