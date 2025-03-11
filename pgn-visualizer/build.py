import PyInstaller.__main__
import sys
import os
import glob

print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")

# Check if main.py exists
if os.path.exists('./src/main.py'):
    print("main.py found")
else:
    print("main.py NOT found")

# Find all PNG files in the current directory
png_files = glob.glob('*.png')
print(f"PNG files found: {png_files}")

import PyInstaller.__main__
import sys
import os

print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")

# Run PyInstaller
PyInstaller.__main__.run([
    './src/main.py',
    '--name=PGN Visualizer',
    '--onefile',
    '--windowed',
    '--add-data=*.png;.',  # For Windows
    # '--add-data=*.png:.',  # For macOS/Linux (uncomment the appropriate one)
    '--debug=all',
    '--clean',
])