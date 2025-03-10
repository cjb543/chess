import sys

from pathlib import Path

from PyQt6.QtCore import QSize, Qt

from PyQt6.QtWidgets import (QApplication, QFileDialog, QVBoxLayout,
                             QHBoxLayout, QWidget, QPushButton,
                             QMainWindow)

def uploadFile(self):
    documents_dir = str(Path.home() / "Documents")
    fname = QFileDialog.getOpenFileName(self, 'Open file', documents_dir)
    if fname[0]:
        self.loadFile(fname[0])

# Error checking and processing of uploaded PGN file
def loadFile(self, filepath):
    try:
        with open(filepath, 'r') as file:
            # Process
            pass
    except Exception as e:
        print(f"Error loading file: {e}")

# Show next board position
def nextMove(self):
    print("Next Move Clicked!")
    
# Show previous board position
def previousMove(self):
    print("Previous Move Clicked!")