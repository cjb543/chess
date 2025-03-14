import PyInstaller.__main__
import glob

# Get all PNG files in the current directory
png_files = glob.glob("*.png")
data_args = []
for png_file in png_files:
    data_args.append(f'--add-data={png_file};.')

base_args = [
    './src/main.py',
    '--name=PGN Visualizer',
    '--onefile',
    '--windowed',
    '--clean',
    '--icon=favicon.ico'
]
# Combine all arguments
all_args = base_args + data_args
PyInstaller.__main__.run(all_args)