from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QSpacerItem
from PyQt6.QtCore import QSize
import sys
from layout_colorwidget import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PGN Visualizer")
        self.setFixedSize(QSize(640,480))

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        
        board_widget = QWidget()
        board_widget.setFixedSize(200,360)

        layout2.addWidget(board_widget)
        layout2.addWidget(Color("yellow"))
        layout2.addWidget(Color("purple"))

        layout1.addLayout(layout2)

        
        layout3.addWidget(Color("red"))
        layout3.addWidget(Color("purple"))
        layout3.addWidget(Color("yellow"))

        # Create a container for the grouped widgets
        grouped_container = QWidget()
        grouped_layout = QVBoxLayout(grouped_container)
        grouped_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        grouped_layout.setSpacing(0)  # Remove spacing between widgets

        # Add widgets to the grouped layout
        red_widget = Color("red")  # SECTION 1
        purple_widget = Color("purple")  # DIRECTLY BELOW LAST WIDGET
        grouped_layout.addWidget(red_widget)
        grouped_layout.addWidget(purple_widget)

        # Set fixed sizes for these specific widgets first
        red_widget.setFixedWidth(180)
        red_widget.setFixedHeight(40)
        purple_widget.setFixedWidth(180)
        purple_widget.setFixedHeight(40)

        # Ensure the container has the right size as well
        grouped_container.setFixedWidth(180)
        grouped_container.setFixedHeight(80)  # Combined height of both widgets

        # Add the container to layout3
        layout3.addWidget(grouped_container)

        layout3.addWidget(Color("yellow"))

        # Set fixed sizes for all widgets directly in layout3
        for i in range(layout3.count()):
            widget = layout3.itemAt(i).widget()
            if widget and widget is not grouped_container:  # Skip the grouped container
                widget.setFixedWidth(180)
                widget.setFixedHeight(40)

        layout1.addLayout(layout3)   
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()