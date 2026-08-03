from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QHBoxLayout,
    QToolBar,
    QStatusBar,
)

from ui.widgets.canvas import Canvas


class MainWindow(QMainWindow):

    def __init__(self, project):
        super().__init__()

        self.project = project

        self.setWindowTitle("LC Stencil Studio")
        self.resize(1600, 900)

        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.create_ui()

    def create_menu(self):

        menubar = self.menuBar()

        menubar.addMenu("File")
        menubar.addMenu("Modifica")
        menubar.addMenu("Visualizza")
        menubar.addMenu("Stencil")
        menubar.addMenu("Materiali")
        menubar.addMenu("Strumenti")
        menubar.addMenu("Aiuto")

    def create_toolbar(self):

        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)

    def create_statusbar(self):

        status = QStatusBar()

        status.showMessage("Pronto")

        self.setStatusBar(status)

    def create_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout = QHBoxLayout()

        central.setLayout(layout)

        left = QListWidget()

        left.addItems([
            "Progetti",
            "Livelli",
            "Materiali",
            "Preset"
        ])

        left.setMaximumWidth(220)

        center = Canvas(self.project)

        right = QListWidget()

        right.addItems([
            "Proprietà",
            "Dimensioni",
            "Bridge",
            "Colori"
        ])

        right.setMaximumWidth(250)

        layout.addWidget(left)
        layout.addWidget(center)
        layout.addWidget(right)