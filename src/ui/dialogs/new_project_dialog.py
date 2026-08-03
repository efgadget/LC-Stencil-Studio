"""
LC Stencil Studio
New Project Dialog
Sprint 009
"""

from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

from core.material_library import MaterialLibrary
from engine.project_manager import ProjectManager


class NewProjectDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.library = MaterialLibrary()

        self.project_manager = ProjectManager()

        self.project = None

        self.setWindowTitle("Nuovo Progetto")

        self.setMinimumWidth(420)

        self.build_ui()

        self.load_materials()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nome progetto"))

        self.project_name = QLineEdit("Nuovo progetto")

        layout.addWidget(self.project_name)

        layout.addWidget(QLabel("Materiale"))

        self.material_combo = QComboBox()

        layout.addWidget(self.material_combo)

        self.material_combo.currentTextChanged.connect(
            self.update_material_info
        )

        self.size_label = QLabel()

        layout.addWidget(self.size_label)

        self.thickness_label = QLabel()

        layout.addWidget(self.thickness_label)

        buttons = QHBoxLayout()

        self.ok_button = QPushButton("Crea Progetto")

        self.cancel_button = QPushButton("Annulla")

        self.ok_button.clicked.connect(self.create_project)

        self.cancel_button.clicked.connect(self.reject)

        buttons.addWidget(self.ok_button)

        buttons.addWidget(self.cancel_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

    def load_materials(self):

        self.material_combo.clear()

        for material in self.library.materials:

            self.material_combo.addItem(material.name)

        if self.material_combo.count():

            self.update_material_info(
                self.material_combo.currentText()
            )

    def update_material_info(self, name):

        material = self.library.get(name)

        if material is None:
            return

        self.size_label.setText(
            f"Dimensioni: {material.width} × {material.height} mm"
        )

        self.thickness_label.setText(
            f"Spessore: {material.thickness} mm"
        )

    def create_project(self):

        self.project = self.project_manager.new_project(
            name=self.project_name.text(),
            material_name=self.material_combo.currentText()
        )

        self.accept()

    def get_project(self):

        return self.project