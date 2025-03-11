from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt

class ChessBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.square_size = 40
        self.board_size = self.square_size * 8
        self.setMinimumSize(200,200)

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
                    color = QColor(240,217,181)
                else:
                    color = QColor(181,136,99)
                painter.fillRect(x, y, self.square_size, self.square_size, color)
