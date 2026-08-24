"""
LC Stencil Studio
Main Window
Release 0.8.0
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QListWidget, QHBoxLayout, QVBoxLayout, QFormLayout,
    QToolBar, QStatusBar, QFileDialog, QDoubleSpinBox, QCheckBox, QPushButton,
    QGroupBox, QMessageBox
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
        self._updating_properties = False
        self.setWindowTitle(f"LC Stencil Studio 0.8.0 - {project.name}")
        self.resize(1600, 900)
        self.create_menu()
        self.create_toolbar()
        self.create_statusbar()
        self.create_ui()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        for text, slot, shortcut in [
            ("Nuovo Progetto", self.new_project, "Ctrl+N"),
            ("Apri Progetto...", self.open_project, "Ctrl+O"),
            ("Salva", self.save_project, "Ctrl+S"),
            ("Salva con nome...", self.save_project_as, "Ctrl+Shift+S"),
        ]:
            action = QAction(text, self)
            action.setShortcut(shortcut)
            action.triggered.connect(slot)
            file_menu.addAction(action)
        file_menu.addSeparator()
        action_import = QAction("Importa immagine...", self)
        action_import.triggered.connect(self.import_image)
        file_menu.addAction(action_import)
        file_menu.addSeparator()
        action_exit = QAction("Esci", self)
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)

        edit_menu = menubar.addMenu("Modifica")
        for text, slot, shortcut in [
            ("Duplica", self.duplicate_selected, "Ctrl+D"),
            ("Elimina", self.delete_selected, "Delete"),
            ("Reset trasformazioni", self.reset_selected, None),
        ]:
            action = QAction(text, self)
            if shortcut:
                action.setShortcut(shortcut)
            action.triggered.connect(slot)
            edit_menu.addAction(action)

        view_menu = menubar.addMenu("Visualizza")
        fit_action = QAction("Adatta vista al materiale", self)
        fit_action.triggered.connect(lambda: self.canvas.fit_material())
        view_menu.addAction(fit_action)
        menubar.addMenu("Stencil")
        menubar.addMenu("Materiali")
        tools_menu = menubar.addMenu("Strumenti")
        center_action = QAction("Centra selezione", self)
        center_action.triggered.connect(self.center_selected)
        tools_menu.addAction(center_action)
        fit_sel_action = QAction("Adatta selezione al materiale", self)
        fit_sel_action.triggered.connect(self.fit_selected)
        tools_menu.addAction(fit_sel_action)
        menubar.addMenu("Aiuto")

    def _confirm_discard_changes(self):
        if not self.project or not self.project.modified:
            return True
        box = QMessageBox(self)
        box.setWindowTitle("LC Stencil Studio")
        box.setIcon(QMessageBox.Icon.Warning)
        box.setText("Il progetto contiene modifiche non salvate.")
        box.setInformativeText("Vuoi salvare le modifiche prima di continuare?")
        box.setStandardButtons(
            QMessageBox.StandardButton.Save |
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )
        box.setDefaultButton(QMessageBox.StandardButton.Save)
        result = box.exec()
        if result == QMessageBox.StandardButton.Save:
            return bool(self.save_project())
        if result == QMessageBox.StandardButton.Discard:
            return True
        return False

    def new_project(self):
        if not self._confirm_discard_changes():
            return
        dialog = NewProjectDialog()
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        self.project = dialog.get_project()
        self.document.set_project(self.project)
        self.canvas.reset_for_project(self.project)
        self.setWindowTitle(f"LC Stencil Studio 0.8.0 - {self.project.name}")
        self.clear_properties()
        self.statusBar().showMessage("Nuovo progetto creato", 3000)

    def open_project(self):
        if not self._confirm_discard_changes():
            return
        filename, _ = QFileDialog.getOpenFileName(self, "Apri progetto", "", "LC Stencil Studio (*.lcs)")
        if not filename:
            return
        project = self.document.load_project(filename)
        if project is None:
            QMessageBox.warning(self, "LC Stencil Studio", "Impossibile aprire il progetto.")
            return
        self.project = project
        self.document.set_project(project)
        self.canvas.reset_for_project(project)
        if project.image_path:
            if self.canvas.import_image(project.image_path):
                g = project.image_geometry
                if g:
                    self.canvas.set_selected_geometry(
                        x=g.get("x"), y=g.get("y"), width=g.get("width"),
                        height=g.get("height"), rotation=g.get("rotation", 0),
                        lock_aspect=False,
                    )
        project.modified = False
        self.setWindowTitle(f"LC Stencil Studio 0.8.0 - {project.name}")
        self.refresh_properties()
        self.statusBar().showMessage("Progetto aperto", 3000)

    def save_project(self):
        if not self.project.file_path:
            return self.save_project_as()
        return self._save_to(self.project.file_path)

    def save_project_as(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Salva progetto", self.project.name, "LC Stencil Studio (*.lcs)")
        if not filename:
            return False
        return self._save_to(filename)

    def _save_to(self, filename):
        geometry = self.canvas.get_selected_geometry()
        image_path = self.canvas.image_engine.image_path
        ok = self.document.save_project(filename, image_path=image_path, image_geometry=geometry)
        if ok:
            # DocumentEngine may normalize the filename (for example adding .lcs).
            # Keep MainWindow bound to the exact same Project instance/path so that
            # subsequent Ctrl+S and Save-on-close overwrite instead of opening Save As.
            self.project = self.document.get_project()
            self.setWindowTitle(f"LC Stencil Studio 0.8.0 - {self.project.name}")
            self.statusBar().showMessage("Progetto salvato", 3000)
            return True
        QMessageBox.warning(self, "LC Stencil Studio", "Impossibile salvare il progetto.")
        return False

    def closeEvent(self, event):
        if self._confirm_discard_changes():
            event.accept()
        else:
            event.ignore()

    def import_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Importa immagine", "", "Immagini (*.png *.jpg *.jpeg *.bmp)")
        if not filename:
            return
        result = self.canvas.import_image(filename)
        if result:
            self.project.image_path = filename
            self.refresh_properties()
            self.statusBar().showMessage("Immagine importata", 3000)
        else:
            self.statusBar().showMessage("Errore importazione immagine", 3000)

    def create_toolbar(self):
        toolbar = QToolBar("CAD")
        self.addToolBar(toolbar)
        for text, slot in [
            ("Importa", self.import_image), ("Centra", self.center_selected),
            ("Duplica", self.duplicate_selected), ("Elimina", self.delete_selected),
            ("Reset", self.reset_selected), ("Adatta materiale", self.fit_selected),
        ]:
            action = QAction(text, self)
            action.triggered.connect(slot)
            toolbar.addAction(action)

    def create_statusbar(self):
        status = QStatusBar()
        status.showMessage("Pronto - Projects 0.8.0")
        self.setStatusBar(status)

    def _spin(self, minimum=-100000.0, maximum=100000.0, decimals=2):
        spin = QDoubleSpinBox()
        spin.setRange(minimum, maximum); spin.setDecimals(decimals); spin.setSuffix(" mm"); spin.setSingleStep(1.0)
        return spin

    def create_ui(self):
        central = QWidget(); self.setCentralWidget(central); layout = QHBoxLayout(central)
        left = QListWidget(); left.addItems(["Progetti", "Livelli", "Materiali", "Preset"]); left.setMaximumWidth(220)
        self.canvas = Canvas(self.project)
        self.canvas.scene.selectionChanged.connect(self.refresh_properties)
        self.canvas.geometryChanged.connect(self.refresh_properties)
        right_container = QWidget(); right_container.setMaximumWidth(300); right_layout = QVBoxLayout(right_container)
        properties = QGroupBox("Proprietà CAD"); form = QFormLayout(properties)
        self.x_spin = self._spin(); self.y_spin = self._spin(); self.w_spin = self._spin(0.01, 100000.0); self.h_spin = self._spin(0.01, 100000.0)
        self.rotation_spin = QDoubleSpinBox(); self.rotation_spin.setRange(-360.0, 360.0); self.rotation_spin.setDecimals(1); self.rotation_spin.setSuffix("°")
        self.aspect_lock = QCheckBox("Mantieni proporzioni"); self.aspect_lock.setChecked(True)
        form.addRow("X", self.x_spin); form.addRow("Y", self.y_spin); form.addRow("Larghezza", self.w_spin); form.addRow("Altezza", self.h_spin); form.addRow("Rotazione", self.rotation_spin); form.addRow(self.aspect_lock)
        apply_btn = QPushButton("APPLICA MISURE"); apply_btn.clicked.connect(self.apply_properties); form.addRow(apply_btn); right_layout.addWidget(properties)
        actions = QGroupBox("Azioni"); actions_layout = QVBoxLayout(actions)
        for text, slot in [("Centra sul materiale", self.center_selected), ("Adatta al materiale", self.fit_selected), ("Duplica", self.duplicate_selected), ("Reset trasformazioni", self.reset_selected), ("Elimina", self.delete_selected)]:
            btn = QPushButton(text); btn.clicked.connect(slot); actions_layout.addWidget(btn)
        right_layout.addWidget(actions); right_layout.addStretch(); layout.addWidget(left); layout.addWidget(self.canvas, 1); layout.addWidget(right_container)

    def clear_properties(self):
        self._updating_properties = True
        for spin in (self.x_spin, self.y_spin, self.w_spin, self.h_spin, self.rotation_spin): spin.setValue(0)
        self._updating_properties = False

    def refresh_properties(self):
        geometry = self.canvas.get_selected_geometry()
        if not geometry: self.clear_properties(); return
        self._updating_properties = True
        self.x_spin.setValue(geometry["x"]); self.y_spin.setValue(geometry["y"]); self.w_spin.setValue(geometry["width"]); self.h_spin.setValue(geometry["height"]); self.rotation_spin.setValue(geometry["rotation"])
        self._updating_properties = False

    def apply_properties(self):
        if self._updating_properties: return
        ok = self.canvas.set_selected_geometry(x=self.x_spin.value(), y=self.y_spin.value(), width=self.w_spin.value(), height=self.h_spin.value(), rotation=self.rotation_spin.value(), lock_aspect=self.aspect_lock.isChecked())
        if ok: self.refresh_properties(); self.statusBar().showMessage("Misure CAD applicate", 2000)

    def center_selected(self):
        if self.canvas.center_selected(): self.refresh_properties(); self.statusBar().showMessage("Selezione centrata", 2000)

    def duplicate_selected(self):
        if self.canvas.duplicate_selected(): self.refresh_properties(); self.statusBar().showMessage("Elemento duplicato", 2000)

    def delete_selected(self):
        if self.canvas.delete_selected(): self.clear_properties(); self.statusBar().showMessage("Elemento eliminato", 2000)

    def reset_selected(self):
        if self.canvas.reset_selected_transform(): self.refresh_properties(); self.statusBar().showMessage("Trasformazioni ripristinate", 2000)

    def fit_selected(self):
        if self.canvas.fit_selected_to_material(): self.refresh_properties(); self.statusBar().showMessage("Selezione adattata al materiale", 2000)
