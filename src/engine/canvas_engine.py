"""
LC Stencil Studio
Canvas Engine
Release 0.6.7
"""

from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QBrush, QPen
from PySide6.QtCore import Qt

from engine.grid_engine import GridEngine


class CanvasEngine:

    def __init__(self, scene):
        self.scene = scene
        self.grid = GridEngine(scene)
        self.material_item = None

    def clear(self):
        self.scene.clear()
        self.material_item = None

    def draw_project(self, project):

        self.clear()
        self.grid.draw()

        if project is None:
            return

        material = project.material

        width = material.width
        height = material.height

        item = QGraphicsRectItem(
            0,
            0,
            width,
            height
        )

        item.setBrush(
            QBrush(Qt.GlobalColor.white)
        )

        item.setPen(
            QPen(Qt.GlobalColor.black, 1)
        )

        item.setPos(
            -width / 2,
            -height / 2
        )

        self.scene.addItem(item)

        self.material_item = item