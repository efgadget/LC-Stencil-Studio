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


class NewProjectDialog(QDialog):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Nuovo Progetto")

        self.setMinimumWidth(420)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        # Nome progetto

        layout.addWidget(QLabel("Nome progetto"))

        self.project_name = QLineEdit()

        self.project_name.setText("Nuovo progetto")

        layout.addWidget(self.project_name)

        # Materiale

        layout.addWidget(QLabel("Materiale"))

        self.material_combo = QComboBox()

        layout.addWidget(self.material_combo)

        # Dimensioni

        self.size_label = QLabel("---")

        layout.addWidget(self.size_label)

        # Spessore

        self.thickness_label = QLabel("---")

        layout.addWidget(self.thickness_label)

        # Pulsanti

        buttons = QHBoxLayout()

        self.ok_button = QPushButton("Crea Progetto")

        self.cancel_button = QPushButton("Annulla")

        buttons.addWidget(self.ok_button)

        buttons.addWidget(self.cancel_button)

        layout.addLayout(buttons)

        self.setLayout(layout)