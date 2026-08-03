from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("LC Stencil Studio")
        self.resize(1400, 900)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()

        title = QLabel("LC STENCIL STUDIO")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Versione Alpha 0.1")
        subtitle.setAlignment(Qt.AlignCenter)

        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

        central.setLayout(layout)
        