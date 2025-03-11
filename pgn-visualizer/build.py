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