from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QHBoxLayout,
    QToolBar,
    QStatusBar,
)

from PySide6.QtGui import QAction

from ui.widgets.canvas import Canvas
from ui.dialogs.new_project_dialog import NewProjectDialog

from engine.document_engine import DocumentEngine


class MainWindow(QMainWindow):

    def __init__(self, project):

        super().__init__()

        self.document = DocumentEngine()
        self.document.set_project(project)

        self.project = project

        self.setWindowTitle(
            f"LC Stencil Studio - {project.name}"
        )

        self.resize(1600, 900)

        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.create_ui()

    def create_menu(self):

        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        action_new = QAction("Nuovo Progetto", self)
        action_new.triggered.connect(self.new_project)

        file_menu.addAction(action_new)

        file_menu.addSeparator()

        action_exit = QAction("Esci", self)
        action_exit.triggered.connect(self.close)

        file_menu.addAction(action_exit)

        menubar.addMenu("Modifica")
        menubar.addMenu("Visualizza")
        menubar.addMenu("Stencil")
        menubar.addMenu("Materiali")
        menubar.addMenu("Strumenti")
        menubar.addMenu("Aiuto")

    def new_project(self):

        dialog = NewProjectDialog()

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        self.project = dialog.get_project()

        self.document.set_project(self.project)

        self.canvas.project = self.project

        self.canvas.engine.draw_project(self.project)

        self.setWindowTitle(
            f"LC Stencil Studio - {self.project.name}"
        )

        self.statusBar().showMessage(
            "Nuovo progetto creato",
            3000
        )

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

        self.canvas = Canvas(self.project)

        right = QListWidget()

        right.addItems([
            "Proprietà",
            "Dimensioni",
            "Bridge",
            "Colori"
        ])

        right.setMaximumWidth(250)

        layout.addWidget(left)
        layout.addWidget(self.canvas)
        layout.addWidget(right)