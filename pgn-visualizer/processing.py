import sys

from pathlib import Path

from PyQt6.QtCore import QSize, Qt

from PyQt6.QtWidgets import (QApplication, QFileDialog, QVBoxLayout,
                             QHBoxLayout, QWidget, QPushButton,
                             QMainWindow)

# When user clicks "Import PGN" and attempts to upload a PGN file
def uploadFile(self):
    documents_dir = str(Path.home() / "Documents")
    fname = QFileDialog.getOpenFileName(self, 'Open file', documents_dir)
    if fname[0]:
        self.loadFile(fname[0])
    # TODO: Error check for proper PGN Notation, file extension etc...

# Error checking and processing of uploaded PGN file
def loadFile(self, filepath):
    try:
        with open(filepath, 'r') as file:
            # Process
            pass
    except Exception as e:
        print(f"Error loading file: {e}")

# Show next board position
def nextMove():
    print("Next Move Clicked!")

# Show previous board position
def previousMove():
    print("Previous Move Clicked!")