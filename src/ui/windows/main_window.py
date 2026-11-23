"""
LC Stencil Studio
Main Window
Release 0.6.7
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QHBoxLayout,
    QToolBar,
    QStatusBar,
    QFileDialog,
    QInputDialog,
    QMessageBox
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

        self.setWindowTitle(f"LC Stencil Studio - {project.name}")
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

        action_import = QAction("Importa immagine...", self)
        action_import.triggered.connect(self.import_image)
        file_menu.addAction(action_import)

        file_menu.addSeparator()

        action_exit = QAction("Esci", self)
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)

        menubar.addMenu("Modifica")
        menubar.addMenu("Visualizza")
        stencil_menu = menubar.addMenu("Stencil")
        action_threshold = QAction("Converti in bianco e nero...", self)
        action_threshold.triggered.connect(self.convert_to_stencil_preview)
        stencil_menu.addAction(action_threshold)

        action_restore = QAction("Ripristina immagine originale", self)
        action_restore.triggered.connect(self.restore_original_image)
        stencil_menu.addAction(action_restore)

        stencil_menu.addSeparator()
        action_bridges = QAction("Anteprima ponticelli automatici...", self)
        action_bridges.triggered.connect(self.preview_auto_bridges)
        stencil_menu.addAction(action_bridges)
        menubar.addMenu("Materiali")
        menubar.addMenu("Strumenti")
        menubar.addMenu("Aiuto")

    def new_project(self):
        dialog = NewProjectDialog()

        if dialog.exec() != dialog.DialogCode.Accepted:
            return

        self.project = dialog.get_project()
        self.document.set_project(self.project)

        # Reset scene, image references, selection and viewport atomically.
        self.canvas.reset_for_project(self.project)

        self.setWindowTitle(
            f"LC Stencil Studio - {self.project.name}"
        )
        self.statusBar().showMessage(
            "Nuovo progetto creato",
            3000
        )

    def import_image(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Importa immagine",
            "",
            "Immagini (*.png *.jpg *.jpeg *.bmp)"
        )

        if not filename:
            return

        result = self.canvas.import_image(filename)

        if result:
            self.statusBar().showMessage(
                "Immagine importata",
                3000
            )
        else:
            self.statusBar().showMessage(
                "Errore importazione immagine",
                3000
            )

    def convert_to_stencil_preview(self):
        if not self.canvas.image_engine.has_image():
            QMessageBox.information(self, "Stencil", "Importa prima un'immagine dal menu File.")
            return

        value, accepted = QInputDialog.getInt(
            self, "Conversione bianco e nero",
            "Soglia (0-255): valori più alti includono più grigi nel nero.",
            self.canvas.image_engine.threshold, 0, 255, 1
        )
        if not accepted:
            return
        if self.canvas.image_engine.apply_threshold(value):
            self.statusBar().showMessage(f"Anteprima bianco/nero - soglia {value}", 5000)
        else:
            QMessageBox.warning(self, "Stencil", "Impossibile convertire l'immagine.")

    def restore_original_image(self):
        if self.canvas.image_engine.restore_original():
            self.statusBar().showMessage("Immagine originale ripristinata", 3000)
        else:
            QMessageBox.information(self, "Stencil", "Non è presente un'immagine da ripristinare.")

    def preview_auto_bridges(self):
        engine = self.canvas.image_engine
        if not engine.has_image():
            QMessageBox.information(self, "Ponticelli", "Importa prima un'immagine.")
            return
        image_width_mm, ok = QInputDialog.getDouble(
            self, "Larghezza del logo", "Larghezza finale del logo (mm):",
            100.0, 1.0, 5000.0, 1
        )
        if not ok:
            return
        bridge_mm, ok = QInputDialog.getDouble(
            self, "Ponticelli automatici", "Larghezza ponticello (mm):",
            1.5, 0.1, 50.0, 2
        )
        if not ok:
            return
        direction, ok = QInputDialog.getItem(
            self, "Posizionamento ponticelli",
            "Preferenza di posizionamento:",
            ["Orizzontale (consigliato per scritte)",
             "Verticale", "Percorso più corto"], 0, False
        )
        if not ok:
            return
        orientation = {
            "Orizzontale (consigliato per scritte)": "horizontal",
            "Verticale": "vertical",
            "Percorso più corto": "shortest"
        }[direction]
        try:
            count = engine.preview_bridges(image_width_mm, bridge_mm, orientation)
        except ValueError as exc:
            QMessageBox.warning(self, "Ponticelli", str(exc))
            return
        self.statusBar().showMessage(
            f"Anteprima: {count} ponticelli automatici. Verificare prima del taglio.",
            8000
        )
        QMessageBox.information(
            self, "Anteprima ponticelli",
            f"Creati {count} ponticelli. Questa è un'anteprima raster, "
            "NON un file pronto per il laser. Controlla ogni lettera."
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
