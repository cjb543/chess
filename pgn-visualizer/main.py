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
        self.setMinimumSize(200, 200)
        
    def resizeEvent(self, event):
        # Calculate the new board size based on available space
        available_space = min(self.width(), self.height())
        self.board_size = available_space - 20  # Leave some margin
        self.square_size = self.board_size // 8

        # Recalculate board size to ensure perfect squares
        self.board_size = self.square_size * 8
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Calculate the centered position for the board
        start_x = (self.width() - self.board_size) // 2
        start_y = (self.height() - self.board_size) // 2
        
        # Draw the chess board
        for row in range(8):
            for col in range(8):
                x = start_x + col * self.square_size
                y = start_y + row * self.square_size
                
                # Set square color (alternate between light and dark)
                if (row + col) % 2 == 0:
                    color = QColor(240, 217, 181)  # Light square
                else:
                    color = QColor(181, 136, 99)   # Dark square
                
                painter.fillRect(x, y, self.square_size, self.square_size, color)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle("Chess Board")
        self.setMinimumSize(400, 400)
        
        # Create a central widget to hold our layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main vertical layout
        main_layout = QVBoxLayout(central_widget)
        
        # Add components to layout
        self.setupTitleSection(main_layout)
        self.setupBoardAndUploadSection(main_layout)
        self.setupNavigationButtons(main_layout)
        
        # Add some margin at the bottom
        main_layout.addSpacing(10)

    def setupTitleSection(self, parent_layout):
        title_label = QLabel("{PLAYER 1 vs. PLAYER 2}")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Styling
        font = QFont("Arial", 16, QFont.Weight.Bold)
        title_label.setFont(font)
        title_label.setMargin(10)
        
        # Add to main layout
        parent_layout.addWidget(title_label)

    def setupBoardAndUploadSection(self, parent_layout):
        # Create horizontal layout
        board_upload_layout = QHBoxLayout()
        parent_layout.addLayout(board_upload_layout)
        
        # Create and add the chess board
        self.chess_board = ChessBoard()
        board_upload_layout.addWidget(self.chess_board, 4)
        
        # Create upload button
        upload_button = QPushButton("Upload")
        upload_button.setMinimumHeight(80)
        upload_button.setCheckable(True)
        upload_button.clicked.connect(self.showUploadDialog)
        board_upload_layout.addWidget(upload_button, 1)

    def setupNavigationButtons(self, parent_layout):
        # Create horizontal layout for arrow buttons
        arrow_layout = QHBoxLayout()
        parent_layout.addLayout(arrow_layout)
        
        # Add spacer to center the arrow buttons
        arrow_layout.addStretch(1)
        
        # Create left arrow button
        left_button = QPushButton("←")
        left_button.setMinimumSize(80, 30)
        left_button.clicked.connect(self.navigateLeft)
        arrow_layout.addWidget(left_button)
        
        # Add spacing between buttons
        arrow_layout.addSpacing(20)
        
        # Create right arrow button
        right_button = QPushButton("→")
        right_button.setMinimumSize(80, 30)
        right_button.clicked.connect(self.navigateRight)
        arrow_layout.addWidget(right_button)
        
        # Add spacer to center the arrow buttons
        arrow_layout.addStretch(1)

    def showUploadDialog(self):
        # Open Downloads dir
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