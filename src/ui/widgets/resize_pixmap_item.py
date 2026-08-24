"""
LC Stencil Studio
Pixmap Item
Release 0.6.7

The item is responsible only for image display, movement and selection.
Resize is handled exclusively by SelectionOverlay.
"""

from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtCore import Qt


class ResizablePixmapItem(QGraphicsPixmapItem):

    def __init__(self, pixmap):

        super().__init__(pixmap)

        self.setFlags(
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsPixmapItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        self.setTransformationMode(
            Qt.TransformationMode.SmoothTransformation
        )
