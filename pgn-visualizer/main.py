import sys
from pathlib import Path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                             QFileDialog,  QVBoxLayout, QHBoxLayout,
                             QLabel,       QPushButton)

from PyQt6.QtGui import (QPainter, QColor, QFont,
                         QAction,  QIcon)

from PyQt6.QtCore import (Qt, QRect, QSize)

class ChessBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.square_size = 40
        self.board_size = self.square_size * 8
        self.setMinimumSize(400, 400)

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("PGN Visualizer")
        self.setFixedSize(640, 480)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        self.setupTitleSection(main_layout)
        self.setupBoardAndUploadSection(main_layout)
        self.setupNavigationButtons(main_layout)

    def setupTitleSection(self, parent_layout):
        player_1, player_2 = "hello", "world"
        title_text = f"{player_1} vs. {player_2}"
        title_label = QLabel(title_text)
        font = QFont("Consolas", 12, QFont.Weight.Bold)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(title_label)

    def setupBoardAndUploadSection(self, parent_layout):
        # Create the main horizontal layout with reduced spacing
        board_upload_layout = QHBoxLayout()
        board_upload_layout.setSpacing(1)  # Reduce default spacing between widgets
        board_upload_layout.setContentsMargins(0, 0, 0, 0)  # Reduce margins
        parent_layout.addLayout(board_upload_layout)

        # Add chess board
        self.chess_board = ChessBoard()
        board_upload_layout.addWidget(self.chess_board, 1)

        # Create a small container for the button with reduced margins
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)  # No margins

        # Create the upload button with reduced size
        upload_button = QPushButton("Upload")
        upload_button.setMinimumHeight(40)
        upload_button.setMaximumWidth(80)  # Limit the width
        upload_button.setCheckable(True)
        upload_button.clicked.connect(self.showUploadDialog)

        # Add button to its container with alignment
        button_layout.addWidget(upload_button, 0, Qt.AlignmentFlag.AlignCenter)

        # Add the button container to the main layout
        board_upload_layout.addWidget(button_container, 1)

    def setupNavigationButtons(self, parent_layout):
        arrow_layout = QHBoxLayout()
        parent_layout.addLayout(arrow_layout)
        arrow_layout.addStretch(1)
        left_button = QPushButton("←")
        left_button.setMinimumSize(80, 30)
        left_button.clicked.connect(self.navigateLeft)
        arrow_layout.addWidget(left_button)
        arrow_layout.addSpacing(20)
        right_button = QPushButton("→")
        right_button.setMinimumSize(80, 30)
        right_button.clicked.connect(self.navigateRight)
        arrow_layout.addWidget(right_button)
        arrow_layout.addStretch(1)

    def showUploadDialog(self):
        documents_dir = str(Path.home() / "Documents")
        fname = QFileDialog.getOpenFileName(self, 'Open file', documents_dir)
        if fname[0]:
            self.loadFile(fname[0])
    
    def loadFile(self, filepath):
        try:
            with open(filepath, 'r') as f:
                # Process PGN file
                pass
        except Exception as e:
            print(f"Error loading file: {e}")
    
    def navigateLeft(self):
        # Go to previous move (or nothing if turn index = 0)
        pass
    
    def navigateRight(self):
        # Go to next move (or nothing if turn index = turns.len())
        pass

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()