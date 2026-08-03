from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QBrush, QPen
from PySide6.QtCore import Qt


class CanvasEngine:
    """
    Motore grafico del Canvas.

    Non conosce la UI.
    Non conosce la MainWindow.

    Riceve un Project e disegna la scena.
    """

    def __init__(self, scene):

        self.scene = scene

        self.material_item = None

    def clear(self):

        self.scene.clear()

        self.material_item = None

    def draw_project(self, project):

        self.clear()

        if project is None:
            return

        material = project.material

        width = material.width
        height = material.height

        self.material_item = QGraphicsRectItem(
            0,
            0,
            width,
            height
        )

        self.material_item.setBrush(
            QBrush(Qt.GlobalColor.white)
        )

        self.material_item.setPen(
            QPen(Qt.GlobalColor.black, 1)
        )

        self.scene.addItem(self.material_item)

        self.material_item.setPos(
            -width / 2,
            -height / 2
        )