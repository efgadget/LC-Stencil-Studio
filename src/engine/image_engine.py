"""
LC Stencil Studio
Image Engine
Release 0.6.1
"""

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from ui.widgets.resize_pixmap_item import ResizablePixmapItem


class ImageEngine:

    def __init__(self, scene):

        self.scene = scene
        self.image_item = None


    def clear(self):

        if self.image_item:

            self.scene.removeItem(
                self.image_item
            )

            self.image_item = None



    def load_image(self, filename):

        self.clear()

        pixmap = QPixmap(filename)

        if pixmap.isNull():

            return False


        self.image_item = ResizablePixmapItem(
            pixmap
        )


        self.image_item.setTransformationMode(
            Qt.TransformationMode.SmoothTransformation
        )


        rect = self.image_item.boundingRect()


        self.image_item.setPos(
            -rect.width() / 2,
            -rect.height() / 2
        )


        self.scene.addItem(
            self.image_item
        )


        return True



    def has_image(self):

        return self.image_item is not None



    def get_image(self):

        return self.image_item