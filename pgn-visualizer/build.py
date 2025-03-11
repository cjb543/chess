''' 
Build file for PyInstaller. 
Just for visual purpose.
Could easily have been done on command line.
'''
import PyInstaller.__main__

PyInstaller.__main__.run([
    './src/main.py',
    '--name=PGN Visualizer',
    '--onefile',
    '--windowed',
    '--add-data=*.png;.',
    '--debug=all',
    '--clean',
])