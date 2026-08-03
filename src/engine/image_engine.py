"""
LC Stencil Studio
Image Engine
Sprint 011
"""

from PySide6.QtWidgets import (
    QGraphicsPixmapItem
)

from PySide6.QtGui import (
    QPixmap
)


class ImageEngine:

    def __init__(self, scene):

        self.scene = scene

        self.image_item = None

    def clear(self):

        if self.image_item:

            self.scene.removeItem(self.image_item)

            self.image_item = None

    def load_image(self, filename):

        self.clear()

        pixmap = QPixmap(filename)

        if pixmap.isNull():
            return False

        self.image_item = QGraphicsPixmapItem(pixmap)

        self.image_item.setFlag(
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable,
            True
        )

        self.image_item.setFlag(
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable,
            True
        )

        self.scene.addItem(self.image_item)

        rect = self.image_item.boundingRect()

        self.image_item.setPos(
            -rect.width()/2,
            -rect.height()/2
        )

        return True